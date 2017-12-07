import logging

from grafana.api import create_dashboard as api_create_dashboard

log = logging.getLogger(__name__)

def create_dashboard(title='No title', refresh='5s', overwrite=True, rows=[]):
    dashboard= {
        "overwrite": overwrite,
        "dashboard": {
            "title": title,
            "refresh": refresh,
            "rows": rows,
            "time": {
                "from": "now-15m",
                "to": "now"
            },
        }
    }
    log.info(dashboard)
    api_create_dashboard(dashboard)
