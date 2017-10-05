import json

import requests
from requests.auth import HTTPBasicAuth

from distribrewed import settings

grafana_url = 'grafana:3000'  # TODO: Do not hardcode
grafana_auth = HTTPBasicAuth(settings.DISTRIBREWED_USER, settings.DISTRIBREWED_PASS)
grafana_headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


def _get_full_path(path):
    return ''.join(['http://', grafana_url, path])


def _generic_get(path):
    r = requests.get(_get_full_path(path), auth=grafana_auth, headers=grafana_headers)
    assert r.status_code == 200, 'API did not return code 200'
    return json.loads(r.content)


def _generic_post(path, data):
    r = requests.post(_get_full_path(path), data=json.dumps(data), auth=grafana_auth, headers=grafana_headers)
    assert r.status_code == 200, 'API did not return code 200'
    return json.loads(r.content)


def _generic_put(path, data):
    r = requests.put(_get_full_path(path), data=json.dumps(data), auth=grafana_auth, headers=grafana_headers)
    assert r.status_code == 200, 'API did not return code 200'
    return json.loads(r.content)


# Data sources

def get_data_sources():
    return _generic_get('/api/datasources')


def post_data_source(datasource):
    return _generic_post('/api/datasources', datasource)


# Organisations

def get_organisations():
    return _generic_get('/api/org')


def get_organisations_by_name(name):
    return _generic_get('/api/orgs/name/{}'.format(name))


def update_organisations_by_id(id, data):
    return _generic_put('/api/orgs/{}'.format(id), data)


# Dashboards
def create_dashboard(dashboard):
    return _generic_post('/api/dashboards/db', dashboard)
