# Import signals in distribrewed.celery to make them work

import logging

import consul
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

from masters.signals import worker_registered, handle_pong, worker_de_registered
from workers.models import Worker, WorkerMethod

log = logging.getLogger(__name__)


@receiver(worker_registered)
def create_or_update_worker(sender, worker_id=None, worker_info=None, worker_methods=None, **kwargs):
    prom = worker_info.get('prometheus_scrape_port')
    defaults = {
        'type': worker_info.get('type'),
        'ip_address': worker_info.get('ip'),
        'prometheus_scrape_port': int(prom) if prom else None,
        'last_registered': timezone.now(),
        'last_answered_ping': None,
        'is_answering_ping': False
    }
    try:
        worker = Worker.objects.get(id=worker_id)
        log.info('Updating worker \'{}\' in database'.format(worker_id))
        Worker.objects.filter(id=worker.id).update(
            **defaults
        )
    except Worker.DoesNotExist:
        log.info('Creating worker \'{}\' in database'.format(worker_id))
        worker = Worker.objects.create(
            id=worker_id,
            **defaults
        )
    for method_name, parameters in worker_methods.items():
        method, _ = WorkerMethod.objects.get_or_create(
            worker=worker,
            name=method_name,
            defaults={
                'parameters': parameters
            }
        )


@receiver(worker_de_registered)
def delete_worker(sender, worker_id=None, worker_info=None, **kwargs):
    Worker.objects.filter(id=worker_id).delete()


@receiver(handle_pong)
def handle_pong(sender, worker_id=None, **kwargs):
    Worker.objects.filter(id=worker_id).update(
        last_answered_ping=timezone.now(),
        is_answering_ping=True
    )


@receiver(post_save, sender=Worker)
def add_worker_to_consul(sender, instance=None, created=None, **kwargs):
    if created:
        consul.Consul(**settings.CONSUL).agent.service.register(
            'workers',
            service_id=instance.id,
            address=instance.ip_address,
            port=instance.prometheus_scrape_port,
            tags=[instance.id]
        )


@receiver(post_delete, sender=Worker)
def remove_worker_from_consul(sender, instance=None, **kwargs):
    consul.Consul(**settings.CONSUL).agent.service.deregister(instance.id)
