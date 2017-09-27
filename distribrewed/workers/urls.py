from django.conf.urls import url

from workers.views import WorkerList, WorkerSingle, WorkerPing

urlpatterns = [
    url(r'^$', WorkerList.as_view(), name='workers-list'),
    url(r'^(?P<pk>[\w-]+)/$', WorkerSingle.as_view(), name='workers-single'),
    url(r'^(?P<pk>[\w-]+)/ping/$', WorkerPing.as_view(), name='workers-ping'),
]
