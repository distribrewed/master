import json
import logging

from distribrewed_core.plugin import get_master_plugin
from django.db.models.signals import post_save
from django.dispatch import receiver

from grafana.models import Alert
from masters.signals import receive_grafana_rows
from workers.models import Worker

log = logging.getLogger(__name__)


@receiver(post_save, sender=Alert)
def send_alert(sender, instance=None, created=None, **kwargs):
    if created:
        # TODO: Use a better method to create the message
        message = '\n'.join([instance.title, '\n'] + [
            json.dumps(e, sort_keys=True, indent=4) for e in instance.evalMatches
        ]).replace('{\n', '').replace('}', '').replace('\n}', '')

        message_workers = Worker.objects.filter(inheritance_chain__contains=['MessageWorker'])

        for worker in message_workers:
            worker.call_method_by_name('send_message', args=[message])


@receiver(post_save, sender=Worker)
def query_worker_for_grafana_rows(sender, instance=None, created=None, **kwargs):
    if created:
        log.info('Quering \'{}\' for grafana rows'.format(instance.id))
        m = get_master_plugin()
        m.command_worker_to_send_grafana_rows(instance.id)


@receiver(receive_grafana_rows)
def reveive_grafana_worker_rows(sender, worker_id=None, rows=None, **kwargs):
    log.info('Received \'{}\' grafana rows'.format(worker_id))
