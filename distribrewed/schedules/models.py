from django.db import models

from workers.models import Worker


class Schedule(models.Model):
    name = models.CharField(max_length=30)

    valid_worker_types = ('ScheduleWorker',)
    worker = models.ForeignKey(Worker, blank=True, null=True, on_delete=models.SET_NULL)

    is_valid = models.BooleanField(default=False)
    validation_message = models.CharField(max_length=100)

    is_paused = models.BooleanField(default=False)
    has_started = models.BooleanField(default=False)
    start_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def validate(self):
        pass  # TODO: Validate worker type


class TemperatureSchedule(Schedule):
    valid_worker_types = ('TemperatureWorker',)


class TemperatureTime(models.Model):
    schedule = models.ForeignKey(TemperatureSchedule, on_delete=models.CASCADE)
    duration = models.DurationField(help_text='01:05:03 = 1 hour, 5 minutes and 3 seconds')
    temperature = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return '{}°C for {}'.format(self.temperature, self.duration)
