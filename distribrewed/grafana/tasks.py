import logging

from celery import signals

from grafana.api import get_data_sources, post_data_source

log = logging.getLogger(__name__)


@signals.worker_ready.connect
def set_default_grafana_datasource(*args, **kwargs):
    log.info('Getting data sources')
    d = get_data_sources()
    if len(d) == 0:
        log.info('No data source, adding default')
        post_data_source({
            "name": "prometheus",
            "type": "prometheus",
            "url": "http://prometheus:9090",  # TODO: Do not hardcode
            "access": "proxy",
            "basicAuth": False,
            "isDefault": True
        })
