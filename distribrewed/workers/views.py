from distribrewed_core.plugin import get_master_plugin
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.response import Response

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


class WorkerPing(GenericAPIView):
    """
    Pings worker
    """

    def get(self, request, pk, format=None):
        get_master_plugin().ping_worker(pk)
        return Response({})
