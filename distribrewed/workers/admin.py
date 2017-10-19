from django.contrib import admin

from utils.admin import CustomChangeFormFunctionMixin
from workers.models import Worker, WorkerMethod


class WorkerMethodInline(admin.TabularInline):
    model = WorkerMethod
    readonly_fields = (
        'name',
        'parameters'
    )
    can_delete = False


@admin.register(Worker)
class WorkerAdmin(CustomChangeFormFunctionMixin, admin.ModelAdmin):
    change_form_template = "admin/worker_change_template.html"
    list_display = (
        'id',
        'type',
        'ip_address',
        'is_registered',
        'is_answering_ping'
    )
    readonly_fields = (
        'id',
        'type',
        'inheritance_chain',
        'ip_address',
        'prometheus_scrape_port',
        'last_registered',
        'is_registered',
        'last_answered_ping',
        'is_answering_ping',
        'events',
        'info'
    )
    exclude = ('grafana_rows',)
    inlines = [
        WorkerMethodInline,
    ]

    # Custom functions

    function_lookup_name = 'worker_func'

    def re_register_worker(self, worker):
        worker.call_method_by_name('register')
