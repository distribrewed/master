# noinspection PyShadowingBuiltins
import logging

from distribrewed_core.tasks import master_plugin
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

log = logging.getLogger(__name__)


# noinspection PyShadowingBuiltins
class TestView(GenericAPIView):
    serializer_class = serializers.Serializer

    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    def get(self, request, id, format=None):
        master_plugin.call_worker_method(
            worker_id='telegram',
            method='telegram_bot_send_message',
            args=['Master sending a message through rabbitmq to telegram worker!!']
        )
        return Response({})
