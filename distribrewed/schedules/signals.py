from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from masters.signals import schedule_finished, worker_registered
from schedules.models import TemperatureSchedule


@receiver(post_save, sender=TemperatureSchedule)  # TODO: Generalize for all schedules
def validate(sender, instance, **kwargs):
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
def update_schedules(sender, worker_id=None, schedule_id=None, **kwargs):
    TemperatureSchedule.objects.filter(uuid=schedule_id).update(
        is_finished=True,
        finish_time=timezone.now()
    )


@receiver(worker_registered)  # TODO: Generalize for all schedules
def update_schedule_status(sender, worker_id=None, worker_info=None, worker_methods=None, **kwargs):
    schedule_id = worker_info.get('info', {}).get('schedule_id')
    is_paused = worker_info.get('info', {}).get('is_paused')
    if schedule_id is not None and is_paused is not None:
        TemperatureSchedule.objects.filter(uuid=schedule_id).update(
            is_paused=is_paused
        )
