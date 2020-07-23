from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    drive = models.OneToOneField(
        "drive_data.Folder",
        on_delete=models.SET_NULL,
        null=True,
        related_name="drive_user",
    )

    def __str__(self):
        return f'"{self.username}" {self.first_name} {self.last_name}'
