from django.apps import AppConfig


class TusUploadConfig(AppConfig):
    name = 'uploads'

    # noinspection PyUnresolvedReferences
    def ready(self):
        # Import receivers
        from . import receivers
