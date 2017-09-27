from distribrewed_core.plugin import get_master_plugin
from django.shortcuts import redirect
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveDestroyAPIView

from workers.models import Worker, WorkerMethod
from workers.serializers import WorkerSerializer, WorkerMethodSerializer


class WorkerList(ListAPIView):
    """
    Returns a list of all workers
    """
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class WorkerSingle(RetrieveDestroyAPIView):
    """
    Returns a single worker
    """
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class WorkerMethods(ListAPIView):
    """
    Get worker methods
    """
    queryset = WorkerMethod.objects.all()
    serializer_class = WorkerMethodSerializer

    def get_queryset(self):
        return self.queryset.filter(worker_id=self.kwargs[self.lookup_field])


class WorkerMethodsSingle(GenericAPIView):
    """
    Call worker method
    """

    # noinspection PyUnusedLocal,PyShadowingBuiltins,PyMethodMayBeStatic
    def get(self, request, pk, name, format=None):
        method = WorkerMethod.objects.get(worker_id=pk, name=name)
        args = []
        for p in method.parameters:
            args += [request.query_params.get(p)]
        get_master_plugin()._call_worker_method(worker_id=pk, all_workers=False, method=name, args=args)
        return redirect('workers-single-methods', pk=pk)


class WorkerSinglePing(GenericAPIView):
    """
    Pings worker
    """

    # noinspection PyUnusedLocal,PyShadowingBuiltins,PyMethodMayBeStatic
    def get(self, request, pk, format=None):
        get_master_plugin().ping_worker(pk)
        return redirect('workers-single', pk=pk)
