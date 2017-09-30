from django.db import models
from django.utils import timezone

from workers.models import Worker


class Schedule(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=30)

    valid_worker_types = ('ScheduleWorker',)
    worker = models.ForeignKey(Worker, blank=True, null=True, on_delete=models.SET_NULL)

    is_valid = models.BooleanField(default=False)
    validation_message = models.CharField(max_length=100)

    is_paused = models.BooleanField(default=False)

    has_started = models.BooleanField(default=False)
    start_time = models.DateTimeField(blank=True, null=True)

    is_finished = models.BooleanField(default=False)
    finish_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def validate(self):
        pass  # TODO: Validate worker type

    def _data_to_worker_representation(self):
        raise NotImplemented('Implement how to structure data for worker')

    def start_schedule(self):
        if self.worker:
            self.worker.call_method_by_name('start_worker', args=[self.pk, self.to_worker_representation])
            Schedule.objects.filter(pk=self.pk).update(
                has_started=True,
                start_time=timezone.now()
            )

    def stop_schedule(self):
        if self.worker:
            self.worker.call_method_by_name('stop_worker')

    def pause_worker(self):
        if self.worker:
            self.worker.call_method_by_name('pause_worker')

    def resume_worker(self):
        if self.worker:
            self.worker.call_method_by_name('resume_worker')


class TemperatureSchedule(Schedule):
    valid_worker_types = ('TemperatureWorker',)


class TemperatureTime(models.Model):
    schedule = models.ForeignKey(TemperatureSchedule, on_delete=models.CASCADE)
    duration = models.DurationField(help_text='01:05:03 = 1 hour, 5 minutes and 3 seconds')
    temperature = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return '{}°C for {}'.format(self.temperature, self.duration)
