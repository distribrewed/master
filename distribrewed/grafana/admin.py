from django.contrib import admin

# Register your models here.
from grafana.models import Alert


@admin.register(Alert)
class TemperatureScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'state',
        'message',
    )
    readonly_fields = (
        'title',
        'ruleId',
        'ruleName',
        'ruleUrl',
        'state',
        'imageUrl',
        'message',
        'evalMatches',
    )
