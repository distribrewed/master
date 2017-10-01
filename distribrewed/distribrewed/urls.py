from django.conf.urls import url, include
from django.contrib import admin

from distribrewed.views import TestView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^grafana/', include('grafana.urls')),
    url(r'^workers/', include('workers.urls')),
    url(r'^master/', include('masters.urls')),
    url(r'^test/$', TestView.as_view()),
]
