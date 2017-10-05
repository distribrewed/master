import json

from grafanalib._gen import DashboardEncoder
from grafanalib.core import Dashboard

from grafana.api import create_dashboard as api_create_dashboard


def dashboard_to_dict(dashboard):
    return {
        'dashboard': json.loads(json.dumps(
            dashboard.to_json_data(),
            sort_keys=True,
            indent=2,
            cls=DashboardEncoder
        ))
    }


def create_dashboard(title=None, rows=None, overwrite=True):
    d = Dashboard(
        title=title,
        rows=rows,
    )
    d = dashboard_to_dict(d)
    d["overwrite"] = overwrite
    api_create_dashboard(d)
