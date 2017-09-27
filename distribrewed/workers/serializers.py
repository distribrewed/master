from rest_framework import serializers

from workers.models import Worker


class WorkerSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name='workers-single', format='html')

    class Meta:
        model = Worker
        fields = '__all__'
