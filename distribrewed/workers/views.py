from distribrewed_core.plugin import get_master_plugin
from django.shortcuts import redirect
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView

from workers.models import Worker
from workers.serializers import WorkerSerializer


class WorkerList(ListAPIView):
    """
    Returns a list of all workers
    """
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class WorkerSingle(RetrieveAPIView):
    """
    Returns a single worker
    """
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class WorkerSinglePing(GenericAPIView):
    """
    Pings worker
    """

    # noinspection PyUnusedLocal,PyShadowingBuiltins,PyMethodMayBeStatic
    def get(self, request, pk, format=None):
        get_master_plugin().ping_worker(pk)
        return redirect('workers-single', pk=pk)
