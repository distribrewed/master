from django.apps import AppConfig


class BrewConfig(AppConfig):
    name = 'brew'

    def ready(self):
        # noinspection PyUnresolvedReferences
        import brew.signals
