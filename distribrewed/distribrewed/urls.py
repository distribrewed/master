from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^admin/', RedirectView.as_view(url='/', permanent=True)),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/docs/', include('rest_framework_docs.urls')),
    url(r'^api/grafana/', include('grafana.urls')),
    url(r'^api/workers/', include('workers.urls')),
    url(r'^api/master/', include('masters.urls')),
    # url(r'^tests/', TestView.as_view()),
    url(r'^', admin.site.urls),
    url(r'^brew/', include('brew.urls')),
]
