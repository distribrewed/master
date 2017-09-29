# noinspection PyShadowingBuiltins
import logging
from datetime import datetime, timedelta

from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from schedules.models import TemperatureSchedule, TemperatureTime

log = logging.getLogger(__name__)


# noinspection PyShadowingBuiltins
class TestView(GenericAPIView):
    serializer_class = serializers.Serializer

    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    def get(self, request, format=None):
        a = TemperatureSchedule.objects.create(
            name='test',
        )
        TemperatureTime.objects.create(
            schedule=a,
            duration=timedelta(minutes=5),
            temperature=90
        )
        return Response({})
