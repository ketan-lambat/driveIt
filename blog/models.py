from django.db import models
from registration.models import User
from django.utils import timezone
# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=264, unique=True,null=False)
    slug = models.SlugField(max_length=264, unique=True, null=False)

    content = models.TextField()
    published_on = models.DateTimeField(blank=True, null=True)
    edited_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-published_on']

    def publish(self):
        self.published_on = timezone.now()
        self.save()

    def update(self):
        self.edited_on = timezone.now()
        self.save()

    def __str__(self):
        return self.title

