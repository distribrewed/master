from rest_framework import serializers
from rest_framework.reverse import reverse

from workers.models import Worker, WorkerMethod


class WorkerMethodHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    def to_representation(self, value):
        i = 0
        q = []
        for p in value.parameters:
            q.append('%s={%s}' % (p, i))
            i += 1
        return reverse(
            self._kwargs['view_name'],
            kwargs={'pk': value.worker_id, 'name': value.name},
            request=self.context['request']
        ) + ('?{}'.format('&'.join(q)) if len(q) > 0 else '')


class WorkerMethodSerializer(serializers.ModelSerializer):
    call = WorkerMethodHyperlinkedIdentityField(view_name='workers-single-methods-single', format='html')

    class Meta:
        model = WorkerMethod
        fields = ('name', 'parameters', 'call',)


class WorkerSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name='workers-single', format='html')
    methods = serializers.HyperlinkedIdentityField(view_name='workers-single-methods', format='html')
    ping = serializers.HyperlinkedIdentityField(view_name='workers-single-ping', format='html')

    class Meta:
        model = Worker
        fields = '__all__'
