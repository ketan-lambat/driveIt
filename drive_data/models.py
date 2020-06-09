from django.db import models
from registration.models import User
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.utils.http import urlunquote as urldecode, urlquote as urlencode
from django.dispatch import receiver


class Item(models.Model):
    name = models.CharField(max_length=257, blank=False, editable=True)
    description = models.CharField(max_length=500, null=True)
    date_created = models.DateTimeField(blank=False, auto_now=True)
    date_uploaded = models.DateTimeField(
        auto_now_add=True, blank=False, editable=False
    )
    date_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class File(Item):
    file = models.FileField(upload_to="uploads/", null=True, default=None)
    file_extension = models.CharField(max_length=10)
    file_type = models.CharField(max_length=20)
    file_size = models.DecimalField(
        max_digits=99, decimal_places=90, validators=[MinValueValidator(0.01)]
    )
    temp_file_id = models.UUIDField(blank=True, null=True)
    location = models.ForeignKey(
        "Folder", on_delete=models.CASCADE, related_name="files"
    )

    def __str__(self):
        return self.name

    class Meta:
        default_related_name = "drive_file"


class Folder(Item):
    class Meta:
        default_related_name = "drive_folder"

    location = models.ForeignKey(
        "Folder",
        on_delete=models.CASCADE,
        related_name="files_folder",
        null=True,
    )

    @property
    def size(self):
        return sum(map(lambda x: x.size, self.files_folder.all())) + sum(
            map(lambda x: x.file_size, self.files.all())
        )

    @property
    def urlpath(self):
        folder = self
        path = []
        while folder.location is not None:
            path.append(urlencode(str(folder.name)))
            folder = folder.location
        return "/".join(path[::-1])

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_drive(sender, instance, **kwargs):
    if kwargs.get("created", False):
        drive = Folder.objects.create(
            name="root",
            description="This is your root Directory",
            author=instance,
            location=None,
        )
        instance.drive = drive
        instance.save()
