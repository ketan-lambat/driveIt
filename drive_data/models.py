from django.db import models
from registration.models import User
from django.core.validators import MinValueValidator


class Item(models.Model):
	name = models.CharField(max_length=257, blank=False, editable=True)
	description = models.CharField(max_length=500, null=True)
	date_created = models.DateTimeField(blank=False, auto_now=True)
	date_uploaded = models.DateTimeField(auto_now_add=True, blank=False, editable=False)
	date_modified = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	location = models.ForeignKey("Directory", on_delete=models.CASCADE)

	# to allow inheritance
	class Meta:
		abstract = True


class File(Item):
	file = models.FileField(upload_to='uploads/', null=False, default=None)
	file_extension = models.CharField(max_length=10)
	file_type = models.CharField(max_length=20)
	file_size = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0.01)])
	location = models.ForeignKey("Folder", on_delete=models.CASCADE, related_name="files")

	def __str__(self):
		return self.name


class Folder(Item):
	# item_count = models.IntegerField(validators=[MinValueValidator(0)])
	# folder_size = models.DecimalField(decimal_places=3, validators=[MinValueValidator(0.0)])
	is_root = False

	def __str__(self):
		return self.name


class Directory(Folder):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	location = None
	is_root = True


class File_Test(models.Model):
	file = models.FileField(upload_to='uploads/', null=False, default=None)
	name = models.CharField(max_length=257, blank=False, editable=True)
