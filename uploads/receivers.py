import logging

from django.dispatch import receiver
from django.core.files import File

from uploads.models import get_upload_model
from uploads.signals import received, saved, finished
from uploads.storage import get_save_handler
from drive_data.models import File as FileModel

logger = logging.getLogger(__name__)


@receiver(received, sender=get_upload_model())
def on_receiving_done(sender, instance, **kwargs):
    logger.debug("on_receiving_done: {}".format(instance))
    save_handler = get_save_handler()
    save_handler(upload=instance).run()


@receiver(saved, sender=get_upload_model())
def on_saving_done(sender, instance, **kwargs):
    logger.debug("on_saving_done: {}".format(instance))


@receiver(finished, sender=get_upload_model())
def on_finished(sender, instance, **kwargs):
    logger.debug('on_finished: {}'.format(instance))
    try:
        f = FileModel.objects.get(temp_file_id=instance.guid)
        file_field = getattr(f, 'file')
        file_field.save(
            instance.filename,
            File(open(instance.uploaded_file.path, 'rb'))
        )
        f.temp_file_id = None
        f.save()
        instance.delete()
        for i in get_upload_model().objects.filter(guid=instance.guid):
            i.delete()
    except FileModel.DoesNotExist:
        pass

