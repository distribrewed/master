from django.db import models


class Worker(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    type = models.CharField(max_length=100, null=True)
    ip_address = models.GenericIPAddressField(protocol='IPv4', null=True)
    prometheus_scrape_port = models.IntegerField(null=True)
    last_registered = models.DateTimeField()
    last_answered_ping = models.DateTimeField(null=True)
    is_answering_ping = models.BooleanField(default=False)

    def __str__(self):
        return '{} {} [{}]'.format(self.type, self.id, self.ip_address)
