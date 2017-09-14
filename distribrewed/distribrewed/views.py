# noinspection PyShadowingBuiltins
import logging

from distribrewed_core.plugin import get_master_plugin
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

log = logging.getLogger(__name__)

distribrewed_master = get_master_plugin()  # type: DistribrewedMaster


# noinspection PyShadowingBuiltins
class TestView(GenericAPIView):
    serializer_class = serializers.Serializer

    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    def get(self, request, id, format=None):
        distribrewed_master.send_telgram_message('Send an awesome message')
        return Response({})
