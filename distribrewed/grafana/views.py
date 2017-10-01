# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from grafana.models import Alert


# noinspection PyShadowingBuiltins
class AlertWebHook(GenericAPIView):
    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    def post(self, request, format=None):
        data = request.data
        Alert.objects.create(
            title=data.get('title'),
            ruleId=data.get('ruleId'),
            ruleName=data.get('ruleName'),
            ruleUrl=data.get('ruleUrl'),
            state=data.get('state'),
            imageUrl=data.get('imageUrl'),
            message=data.get('message'),
            evalMatches=data.get('evalMatches')
        )
        return Response({})
