from django.apps import AppConfig


class MasterConfig(AppConfig):
    name = 'masters'

    def ready(self):
        # noinspection PyUnresolvedReferences
        import masters.signals
