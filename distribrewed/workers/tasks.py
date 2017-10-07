import logging
# noinspection PyPackageRequirements
from time import sleep

from celery.task import periodic_task
from distribrewed_core.plugin import get_master_plugin
from django.utils import timezone

from workers.models import Worker

log = logging.getLogger(__name__)


@periodic_task(run_every=timezone.timedelta(seconds=30), routing_key='master')
def check_worker_ping():
    log.info("Checking worker ping")
    m = get_master_plugin()
    for worker in Worker.objects.all():
        m.ping_worker(all_workers=True)
        sleep(10)
        if worker.last_answered_ping is None:
            Worker.objects.filter(id=worker.id).update(is_answering_ping=False)
        elif timezone.now() - worker.last_answered_ping > timezone.timedelta(seconds=45):
            log.info("Worker \'{}\' is not answering ping".format(worker.id))
            Worker.objects.filter(id=worker.id).update(is_answering_ping=False)
