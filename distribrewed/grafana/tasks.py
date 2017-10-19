import logging

from celery import signals
from django.conf import settings

from grafana.api import get_data_sources, post_data_source, get_organisations_by_name, \
    update_organisations_by_id

log = logging.getLogger(__name__)


@signals.worker_ready.connect
def set_default_grafana_datasource(*args, **kwargs):
    log.debug('Getting data sources')
    d = get_data_sources()
    if len(d) == 0:
        log.info('No grafana data source, adding default')
        post_data_source({
            "name": "prometheus",
            "type": "prometheus",
            "url": "http://{}:{}".format(settings.PROMETHEUS['host'], str(settings.PROMETHEUS['port'])),
            "access": "proxy",
            "basicAuth": False,
            "isDefault": True
        })


@signals.worker_ready.connect
def set_default_grafana_org(*args, **kwargs):
    log.debug('Getting organizations')
    try:
        d = get_organisations_by_name('Main Org.')
        log.info('Rename Main Org.')
        update_organisations_by_id(d['id'], {'name': 'distribrewed'})
    except Exception as e:
        pass
