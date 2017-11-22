# Import signals in distribrewed.celery to make them work

import logging

import consul
from consul.base import CB
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
        'inheritance_chain': worker_info.get('inheritance_chain'),
        'ip_address': worker_info.get('ip'),
        'prometheus_scrape_port': int(prom) if prom else None,
        'last_registered': timezone.now(),
        'is_registered': True,
        'last_answered_ping': None,
        'is_answering_ping': False,
        'events': worker_info.get('events'),
        'info': worker_info.get('info')
    }
    try:
        worker = Worker.objects.get(id=worker_id)
        log.info('Updating worker \'{}\' in database'.format(worker_id))
        Worker.objects.filter(id=worker.id).update(
            **defaults
        )
        worker = Worker.objects.get(id=worker_id)
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
    consul_add(worker.id)


@receiver(worker_de_registered)
def mark_worker_as_de_registered(sender, worker_id=None, worker_info=None, **kwargs):
    Worker.objects.filter(id=worker_id).update(
        is_registered=False
    )

    # Remove from consul
    w = Worker.objects.filter(id=worker_id)
    if len(w) == 1:
        consul_remove(w[0])


@receiver(handle_pong)
def handle_pong(sender, worker_id=None, **kwargs):
    Worker.objects.filter(id=worker_id).update(
        last_answered_ping=timezone.now(),
        is_answering_ping=True
    )


@receiver(post_save, sender=Worker)
def add_worker_to_consul(sender, instance=None, created=None, **kwargs):
    if created:
        consul_add(instance.id)


@receiver(post_delete, sender=Worker)
def remove_worker_from_consul(sender, instance=None, **kwargs):
    consul_remove(instance)


def consul_add(worker_id):
    worker = Worker.objects.get(id=worker_id)
    consul.Consul(**settings.CONSUL).agent.service.register(
        'workers',
        service_id=worker.id,
        address=worker.ip_address,
        port=worker.prometheus_scrape_port,
        tags=[worker.id]
    )


def consul_remove(worker):
    service = consul.Consul(**settings.CONSUL).agent.service
    service.agent.http.put(CB.bool(), '/v1/agent/service/deregister/%s' % worker.id)
