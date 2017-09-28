from django.apps import AppConfig


class SchedulesConfig(AppConfig):
    name = 'schedules'

    def ready(self):
        # noinspection PyUnresolvedReferences
        import schedules.signals
