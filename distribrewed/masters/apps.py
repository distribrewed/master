from django.apps import AppConfig


class MasterConfig(AppConfig):
    name = 'masters'

    def ready(self):
        # noinspection PyUnresolvedReferences
        import masters.signals
        self.create_super_user()

    @staticmethod
    def create_super_user():
        # noinspection PyBroadException
        try:
            from django.contrib.auth.models import User
            if len(User.objects.all()) == 0:
                User.objects.create_superuser('admin', '', 'admin')
        except Exception:
            pass
