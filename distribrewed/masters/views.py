from distribrewed_core.plugin import get_master_plugin
from django.shortcuts import redirect
from rest_framework.generics import GenericAPIView


class MasterForceRegister(GenericAPIView):
    """
    Force workers to register
    """

    # noinspection PyUnusedLocal,PyShadowingBuiltins,PyMethodMayBeStatic
    def get(self, request, format=None):
        get_master_plugin().command_all_workers_to_register()
        return redirect('workers-list')
