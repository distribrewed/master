from django.contrib import admin

from workers.models import Worker, WorkerMethod


class WorkerMethodInline(admin.TabularInline):
    model = WorkerMethod
    readonly_fields = (
        'name',
        'parameters'
    )
    can_delete = False


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
        'inheritance_chain',
        'ip_address',
        'prometheus_scrape_port',
        'last_registered',
        'last_answered_ping',
        'is_answering_ping',
        'info'
    )
    inlines = [
        WorkerMethodInline,
    ]
