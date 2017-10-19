from grafana.api import create_dashboard as api_create_dashboard


def create_dashboard(title='No title', refresh='5s', overwrite=True, rows=[]):
    api_create_dashboard({
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
    })
