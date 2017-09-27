from django.apps import AppConfig


class WorkersConfig(AppConfig):
    name = 'workers'

    def ready(self):
        # noinspection PyUnresolvedReferences
        import workers.signals
