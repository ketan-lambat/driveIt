import logging

from django.dispatch import receiver

from uploads.models import get_upload_model
from uploads.signals import received, saved, finished
from uploads.storage import get_save_handler

logger = logging.getLogger(__name__)


@receiver(received, sender=get_upload_model())
def on_receiving_done(sender, instance, **kwargs):
    logger.debug('on_receiving_done: {}'.format(instance))
    save_handler = get_save_handler()
    save_handler(upload=instance).run()


@receiver(saved, sender=get_upload_model())
def on_saving_done(sender, instance, **kwargs):
    logger.debug('on_saving_done: {}'.format(instance))

#
# @receiver(finished, sender=get_upload_model())
# def on_finished(sender, instance, **kwargs):
#     logger.debug('on_finished: {}'.format(instance))
#
