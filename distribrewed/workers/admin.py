from django.contrib import admin

from workers.models import Worker


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'type',
        'ip_address',
        'is_answering_ping'
    )
    readonly_fields = (
        'id',
        'type',
        'ip_address',
        'prometheus_scrape_port',
        'last_registered',
        'last_answered_ping',
        'is_answering_ping',
    )
