from django.db import models
from django.utils import timezone

from utils.models import create_uuid
from workers.models import Worker


class Schedule(models.Model):
    class Meta:
        abstract = True

    uuid = models.CharField(max_length=32, default=create_uuid)
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

    was_stopped = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def validate(self):
        pass  # TODO: Validate worker type

    def _data_to_worker_representation(self):
        raise NotImplemented('Implement how to structure data for worker')

    def start_schedule(self):
        if self.worker:
            self.worker.call_method_by_name('start_worker', args=[self.uuid, self._data_to_worker_representation()])
            self.__class__.objects.filter(pk=self.pk).update(
                has_started=True,
                start_time=timezone.now()
            )

    def stop_schedule(self):
        if self.worker:
            self.worker.call_method_by_name('stop_worker')
        self.__class__.objects.filter(pk=self.pk).update(
            was_stopped=True,
            is_finished=True,
            finish_time=timezone.now()
        )

    def restart_schedule(self):
        self.__class__.objects.filter(pk=self.pk).update(
            was_stopped=False,
            is_finished=False,
            finish_time=None
        )
        self.start_schedule()

    def pause_worker(self):
        if self.worker:
            self.worker.call_method_by_name('pause_worker')

    def resume_worker(self):
        if self.worker:
            self.worker.call_method_by_name('resume_worker')

    def reset_schedule(self):
        self.__class__.objects.filter(pk=self.pk).update(
            has_started=False,
            start_time=None,
            was_stopped=False,
            is_finished=False,
            finish_time=None,
            is_paused=False,
        )
        self.validate()


class TemperatureSchedule(Schedule):
    valid_worker_types = ('TemperatureWorker',)

    def _data_to_worker_representation(self):
        return [(str(t.duration), t.temperature) for t in self.temperaturetime_set.all()]


class TemperatureTime(models.Model):
    schedule = models.ForeignKey(TemperatureSchedule, on_delete=models.CASCADE)
    duration = models.DurationField(help_text='01:05:03 = 1 hour, 5 minutes and 3 seconds')
    temperature = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return '{}°C for {}'.format(self.temperature, self.duration)
