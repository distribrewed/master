from django.contrib import admin

from brew.models import TemperatureSchedule, TemperatureTime, Session, Schedule, Event, EventAction
from brew.models import Recipe, RecipeSection, RecipeStep
from utils.admin import CustomChangeFormFunctionMixin


# Session Admin

class ScheduleInline(admin.TabularInline):
    model = Schedule
    exclude = (
        'uuid',
        'validation_message',

    )
    readonly_fields = (
        'name',
        'worker',
        'is_valid',
        'is_paused',
        'has_started',
        'start_time',
        'is_finished',
        'finish_time',
        'was_stopped',
        'event_names',
        'event_actions',
    )
    show_change_link = True  # TODO: Not working because of model inheritance?
    can_delete = True
    max_num = 0


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )

    inlines = [
        ScheduleInline,
    ]


# Schedule Admin

class EventInline(admin.TabularInline):
    model = Event
    readonly_fields = (
        'name',
    )
    can_delete = False
    max_num = 0


class EventActionInline(admin.TabularInline):
    model = EventAction


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
        'uuid',
        'is_valid',
        'validation_message',
        'has_started',
        'start_time',
        'is_paused',
        'is_finished',
        'finish_time',
        'was_stopped'
    )
    exclude = (
        'send_event',
    )

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.has_started and not obj.is_finished and obj.worker is not None:
            return ('worker',) + self.readonly_fields
        return self.readonly_fields

    def render_change_form(self, request, context, *args, **kwargs):
        # TODO: Only show workers
        return super(ScheduleAdmin, self).render_change_form(request, context, args, kwargs)

    # Custom functions

    function_lookup_name = 'schedule_func'

    def start(self, model):
        model.start_schedule()

    def stop(self, model):
        model.stop_schedule()

    def restart(self, model):
        model.restart_schedule()

    def pause(self, model):
        model.pause_worker()

    def resume(self, model):
        model.resume_worker()

    def reset_schedule(self, model):
        model.reset_schedule()

    inlines = [
        EventInline
    ]


class TemperatureTimeInline(admin.TabularInline):
    model = TemperatureTime


@admin.register(TemperatureSchedule)
class TemperatureScheduleAdmin(ScheduleAdmin):
    inlines = [
        TemperatureTimeInline,
        EventInline,
        # EventActionInline, # TODO: Use generic relations for this to work
    ]

# Recipe admin

class RecipeSectionInline(admin.TabularInline):
    model = RecipeSection


class RecipeStepInline(admin.TabularInline):
    model = RecipeStep


@admin.register(Recipe)
class RecipeAdmin(CustomChangeFormFunctionMixin, admin.ModelAdmin):
    change_list_template = "admin/recipe_change_list_template.html"

    # Custom functions

    function_lookup_name = 'recipe_func'

    inlines = [
        RecipeSectionInline,
        #RecipeStepInline,
    ]
