from django.conf.urls import url, include
from django.contrib import admin

from distribrewed.views import TestView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^(?P<id>.*)$', TestView.as_view(), name='task-run'),
]
