from distribrewed_core.plugin import get_master_plugin
from django.contrib.postgres.fields import ArrayField, HStoreField
from django.db import models


class Worker(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    type = models.CharField(max_length=100, null=True)
    inheritance_chain = ArrayField(models.CharField(max_length=50))
    ip_address = models.GenericIPAddressField(protocol='IPv4', null=True)
    prometheus_scrape_port = models.IntegerField(null=True)
    last_registered = models.DateTimeField()
    is_registered = models.BooleanField(default=False)
    last_answered_ping = models.DateTimeField(null=True)
    is_answering_ping = models.BooleanField(default=False)
    events = ArrayField(models.CharField(max_length=100), default=[])
    info = HStoreField()

    @property
    def methods(self):
        return self.workermethod_set.all()

    def get_method_by_name(self, name):
        return self.methods.get(name=name)

    def call_method_by_name(self, name, args=[]):
        self.get_method_by_name(name).call_method(args=args)

    def __str__(self):
        return '{} [{}] {}'.format(self.id, self.ip_address, self.type)


class WorkerMethod(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    parameters = ArrayField(models.CharField(max_length=30))

    def call_method(self, args=[]):
        assert len(self.parameters) == len(args), 'Invalid number of parameters'
        # noinspection PyProtectedMember
        get_master_plugin()._call_worker_method(worker_id=self.worker_id, method=self.name, args=args)

    def __str__(self):
        return '{}.{}({})'.format(self.worker.type, self.name, ', '.join(self.parameters))
