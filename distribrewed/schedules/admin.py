from django.contrib import admin

from schedules.models import TemperatureSchedule, TemperatureTime
from utils.admin import CustomChangeFormFunctionMixin


class ScheduleAdmin(CustomChangeFormFunctionMixin, admin.ModelAdmin):
    change_form_template = "admin/schedule_change_template.html"
    list_display = (
        'name',
        'has_started',
        'start_time',
        'is_paused',
        'is_valid',
        'validation_message',
        'is_finished',
        'finish_time'
    )
    readonly_fields = (
        'has_started',
        'start_time',
        'is_paused',
        'is_valid',
        'validation_message',
        'is_finished',
        'finish_time'
    )

    def render_change_form(self, request, context, *args, **kwargs):
        # TODO: Only show workers
        return super(ScheduleAdmin, self).render_change_form(request, context, args, kwargs)

    # Custom functions

    function_lookup_name = 'schedule_func'

    def start(self, model):
        model.start_schedule()

    def stop(self, model):
        model.stop_schedule()

    def pause(self, model):
        model.pause_worker()

    def resume(self, model):
        model.pause_worker()


class TemperatureTimeInline(admin.TabularInline):
    model = TemperatureTime


@admin.register(TemperatureSchedule)
class TemperatureScheduleAdmin(ScheduleAdmin):
    inlines = [
        TemperatureTimeInline,
    ]
