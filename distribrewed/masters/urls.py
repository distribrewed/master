from django.conf.urls import url

from masters.views import MasterForceRegister

urlpatterns = [
    url(r'^register_workers/$', MasterForceRegister.as_view(), name='master-register'),
]
