import json

from django.db.models.signals import post_save
from django.dispatch import receiver

from grafana.models import Alert
from workers.models import Worker


@receiver(post_save, sender=Alert)
def send_alert(sender, instance=None, created=None, **kwargs):
    if created:
        # TODO: Use a better method to create the message
        message = '\n'.join([instance.title, '\n'] + [
            json.dumps(e, sort_keys=True, indent=4) for e in instance.evalMatches
        ]).replace('{\n', '').replace('}', '').replace('\n}', '')

        message_workers = Worker.objects.filter(inheritance_chain__contains=['MessageWorker'])

        for worker in message_workers:
            worker.call_method_by_name('send_message', args=[message])
