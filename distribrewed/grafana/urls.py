from django.conf.urls import url

from grafana.views import AlertWebHook

urlpatterns = [
    url(r'^webhook/$', AlertWebHook.as_view(), name='grafana-webhook'),
]
