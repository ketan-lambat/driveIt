from django.apps import AppConfig


class TusUploadConfig(AppConfig):
    name = "uploader"

    # noinspection PyUnresolvedReferences
    def ready(self):
        # Import receivers
        from . import receivers
