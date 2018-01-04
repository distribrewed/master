from django.db import models
from django.utils import timezone

from grafana.dashboards import create_dashboard
from utils.models import create_uuid
from workers.models import Worker, WorkerMethod


class Session(models.Model):
    name = models.CharField(max_length=30)

    def create_grafana_dashboard(self):
        rows = []
        for s in self.schedule_set.all():
            if s.worker:
                rows += s.worker.grafana_rows
        create_dashboard(title=self.name, rows=rows)

    def __str__(self):
        return self.name


# Generic schedule

class Schedule(models.Model):
    uuid = models.CharField(max_length=32, default=create_uuid)
    name = models.CharField(max_length=30)

    session = models.ForeignKey(Session, blank=True, null=True, on_delete=models.SET_NULL)

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

    @property
    def event_names(self):
        return ', '.join([e.name for e in self.event_set.all()])

    @property
    def event_actions(self):
        return ', '.join([str(ea) for ea in self.eventaction_set.all()])

    def validate(self):
        pass  # TODO: Validate worker type

    def _data_to_worker_representation(self):
        raise NotImplemented('Implement how to structure data for worker')

    def start_schedule(self):
        if self.session:
            self.session.create_grafana_dashboard()
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


# Events
# TODO: GENERALIZE SO IT WORKS WITH INHERITANCE

class Event(models.Model):
    name = models.CharField(max_length=30)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return '{}{} [{}] {}'.format(
            '{} - '.format(self.schedule.session) if self.schedule.session else '',
            self.schedule,
            self.schedule.worker.id if self.schedule.worker else 'NO_WORKER',
            self.name
        )


class EventAction(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    action = models.ForeignKey(WorkerMethod, on_delete=models.CASCADE)

    def __str__(self):
        return ' => '.join([
            str(self.event),
            str(self.action.name)
        ])


# Temperature schedules

class TemperatureSchedule(Schedule):
    valid_worker_types = ('TemperatureWorker','DebugTemperatureWorker')

    def _data_to_worker_representation(self):
        return [(str(t.duration), t.temperature) for t in self.temperaturetime_set.all()]


class TemperatureTime(models.Model):
    schedule = models.ForeignKey(TemperatureSchedule, on_delete=models.CASCADE)
    duration = models.DurationField(help_text='01:05:03 = 1 hour, 5 minutes and 3 seconds')
    temperature = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return '{}°C for {}'.format(self.temperature, self.duration)

# Recipies

COLUMN_SMALL_SIZE = 128


class Recipe(models.Model):
    name = models.CharField(max_length=COLUMN_SMALL_SIZE)
    brewer = models.CharField(max_length=COLUMN_SMALL_SIZE)
    style = models.CharField(max_length=COLUMN_SMALL_SIZE)
    category = models.CharField(max_length=COLUMN_SMALL_SIZE)
    description = models.TextField()
    profile = models.TextField()
    ingredients = models.TextField()
    web_link = models.CharField(max_length=COLUMN_SMALL_SIZE)

    def __str__(self):
        return '{0} ({1}) by {2}'.format(self.name, self.style, self.brewer)

    class Meta:
        ordering = ['name']

    def _to_session(self):
        session = Session()
        session.name = self.name
        session.save()
        recipe_sections = RecipeSection.objects.select_related('recipe')
        for section in recipe_sections:
            schedule = TemperatureSchedule()
            schedule.session = session
            schedule.name = section.name
            schedule.save()
            recipe_steps = RecipeStep.objects.select_related('recipesection')
            for step in recipe_steps:
                time = TemperatureTime()
                time.schedule = schedule
                time.temperature = step.target
                time.duration = step.hold_time
                time.save()


class RecipeSection(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    index = models.IntegerField()
    name = models.CharField(max_length=COLUMN_SMALL_SIZE)
    worker_type = models.CharField(max_length=COLUMN_SMALL_SIZE)

    def __str__(self):
        return '{0} using {1}'.format(self.name, self.worker_type)

    class Meta:
        ordering = ['index']


class RecipeStep(models.Model):
    SECONDS = 1
    MINUTES = 60
    HOURS = 60 * MINUTES
    DAYS = 24 * HOURS
    HOLD_TIME_UNITS = (
        (SECONDS, 'Seconds'),
        (MINUTES, 'Minutes'),
        (HOURS, 'Hours'),
        (DAYS, 'Days')
    )
    recipesection = models.ForeignKey(RecipeSection, on_delete=models.CASCADE)
    index = models.IntegerField()
    name = models.CharField(max_length=COLUMN_SMALL_SIZE)
    unit = models.CharField(max_length=COLUMN_SMALL_SIZE)
    target = models.FloatField(max_length=COLUMN_SMALL_SIZE)
    hold_time = models.IntegerField(default=1)
    time_unit_seconds = models.IntegerField(choices=HOLD_TIME_UNITS, default=MINUTES)

    def __str__(self):
        return '{0} with target {1}'.format(self.name, self.target)

    class Meta:
        ordering = ['index']

