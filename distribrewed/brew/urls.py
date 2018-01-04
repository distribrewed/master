from django.conf.urls import url
from brew.views import import_recipe

urlpatterns = [
    url(r'^import_recipe/$', import_recipe),
]