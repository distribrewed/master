from django.contrib import admin, messages

# Register your models here.
from schedules.models import TemperatureSchedule, TemperatureTime


class TemperatureTimeInline(admin.TabularInline):
    model = TemperatureTime


@admin.register(TemperatureSchedule)
class TemperatureScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )

    inlines = [
        TemperatureTimeInline,
    ]

    def save_model(self, request, obj, form, change):
        super(TemperatureScheduleAdmin, self).save_model(request, obj, form, change)
        obj = TemperatureSchedule.objects.get(pk=obj.pk)
        t1 = None
        for temp_time in obj.temperaturetime_set.all():
            t2 = temp_time.timestamp
            if t1 is not None:
                if t1 > t2:
                    messages.add_message(request, messages.ERROR, 'Timestamps not in correct order')
            t1 = t2
