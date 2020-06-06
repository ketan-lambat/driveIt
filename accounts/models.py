from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from registration.models import User
import re


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    pass


@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.create(user=instance)
