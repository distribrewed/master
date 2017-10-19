# noinspection PyShadowingBuiltins
import logging

from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

log = logging.getLogger(__name__)


# noinspection PyShadowingBuiltins
class TestView(GenericAPIView):
    serializer_class = serializers.Serializer

    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    def get(self, request, format=None):
        return Response({})
