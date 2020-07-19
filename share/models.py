import uuid
from django.db import models


class SharedItem(models.Model):
    class Permission(models.TextChoices):
        PUBLIC = 'P', 'Public'
        SELECTIVE = 'S', 'Selective'

    public_id = models.UUIDField(default=uuid.uuid4, unique=True)
    item = models.OneToOneField('drive_data.Item', on_delete=models.CASCADE)
    permission = models.CharField(max_length=1,
                                  choices=Permission.choices,
                                  default=Permission.SELECTIVE)
    access_user = models.ManyToManyField('registration.User')

    def link(self):
        from django.urls import reverse
        return 'http://127.0.0.1:8000'+reverse('shared_view', kwargs={'guid':
                                                                     self.public_id})
