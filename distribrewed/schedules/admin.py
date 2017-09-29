from django.contrib import admin

# Register your models here.
from schedules.models import TemperatureSchedule, TemperatureTime


class ScheduleAdmin(admin.ModelAdmin):
    readonly_fields = (
        'is_valid',
        'validation_message',
        'is_paused',
        'has_started',
        'start_time',
    )


class TemperatureTimeInline(admin.TabularInline):
    model = TemperatureTime


@admin.register(TemperatureSchedule)
class TemperatureScheduleAdmin(ScheduleAdmin):
    list_display = (
        'name',
    )

    inlines = [
        TemperatureTimeInline,
    ]
