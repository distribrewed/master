from django.contrib import admin

# Register your models here.
from schedules.models import TemperatureSchedule, TemperatureTime


class ScheduleAdmin(admin.ModelAdmin):
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


class TemperatureTimeInline(admin.TabularInline):
    model = TemperatureTime


@admin.register(TemperatureSchedule)
class TemperatureScheduleAdmin(ScheduleAdmin):
    inlines = [
        TemperatureTimeInline,
    ]
