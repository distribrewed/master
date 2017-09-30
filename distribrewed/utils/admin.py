from time import sleep

from django.conf.urls import url
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.http import HttpResponseRedirect


class CustomChangeFormFunctionMixin(object):
    function_lookup_name = 'custom_functions'

    def get_urls(self):
        urls = super(CustomChangeFormFunctionMixin, self).get_urls()
        return urls[:-1] + [
            url(r'^(.+)/(.+)/$', self.handle_request, name=self.function_lookup_name)
        ] + [urls[-1]]

    def handle_request(self, request, pk, func):
        getattr(self, func)(self.model.objects.get(pk=pk))

        # Do this part better
        sleep(0.5)
        preserved_filters = self.get_preserved_filters(request)
        redirect_url = request.path.replace('/{}/'.format(func), '')
        redirect_url = add_preserved_filters({'preserved_filters': preserved_filters}, redirect_url)
        return HttpResponseRedirect(redirect_url)
