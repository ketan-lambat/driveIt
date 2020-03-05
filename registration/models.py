from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    drive = models.OneToOneField('drive_data.Folder', on_delete=models.SET_NULL, null=True)

