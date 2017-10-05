from django.apps import AppConfig


class GrafanaConfig(AppConfig):
    name = 'grafana'

    def ready(self):
        # noinspection PyUnresolvedReferences
        import grafana.signals
        # noinspection PyUnresolvedReferences
        import grafana.tasks
