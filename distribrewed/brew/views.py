import os
import logging

from django.http import HttpResponseRedirect

from importing.beer_smith_importer import BeerSmithImporter

log = logging.getLogger(__name__)


# Create your views here.

def import_recipe(request):
    uri = None
    try:
        if request.POST:
            #index = int(request.POST['index'])
            file = request.FILES['file']
            filename = request.FILES['file'].name
            uri = os.path.dirname(os.path.realpath(__file__))
            uri = uri[0:uri.rindex('/')]
            uri += '/importing/uploaded_files/'
            uri += filename
            fd = open(uri, 'wb')
            for chunk in file.chunks():
                fd.write(chunk)
            fd.close()
            brew_importer = BeerSmithImporter()
            brew_importer.do_import(uri)
    except Exception as e:
        try:
            if uri is not None:
                log.error('Failed to upload file {0} : {1}'.format(uri, e.args[0]))
            else:
                log.error('Failed to upload file : {0}'.format(e.args[0]))
        except Exception:
            if uri is not None:
                log.error('Failed to upload file {0}'.format(uri))
            else:
                log.error('Failed to upload file')
    return HttpResponseRedirect('/brew/recipe/')
