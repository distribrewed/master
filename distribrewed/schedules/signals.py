from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from masters.signals import schedule_finished
from schedules.models import TemperatureSchedule


@receiver(post_save, sender=TemperatureSchedule)  # TODO: Generalize for all schedules
def validate(sender, instance, **kwargs):
    update = {}
    try:
        instance.validate()
        update = {
            'is_valid': True,
            'validation_message': 'OK'
        }
    except AssertionError as e:
        update = {
            'is_valid': False,
            'validation_message': e
        }
    TemperatureSchedule.objects.filter(pk=instance.pk).update(
        **update
    )


@receiver(schedule_finished)  # TODO: Generalize for all schedules
def update_temp_schedules(sender, worker_id=None, schedule_id=None, **kwargs):
    TemperatureSchedule.objects.filter(pk=schedule_id).update(
        is_finished=True,
        finish_time=timezone.now()
    )
