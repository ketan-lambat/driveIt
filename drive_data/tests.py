from django.test import TestCase, RequestFactory
from django.urls import resolve, reverse
from django.views import generic
from registration.models import User
from django.contrib.auth.decorators import login_required
from io import BytesIO
from PIL import Image
# from django.core.files.base import File
from .models import File
from .views import (
	DriveDataView,
	FolderDataView,
	file_upload_view,
	create_folder_view,
	file_delete_view,
	folder_delete_view,
)


class CreateUser(TestCase):
	def test_create_user(self):
		user = User.objects.create_user(
			username="testuser", password="test.pass"
		)
		self.assertEqual(user.username, "testuser")
		self.assertTrue(user.is_active)
		self.assertFalse(user.is_staff)
		self.assertFalse(user.is_superuser)

	def test_create_superuser(self):
		admin_user = User.objects.create_superuser(
			username="admin", password="admin.pass"
		)
		self.assertEqual(admin_user.username, "admin")
		self.assertTrue(admin_user.is_active)
		self.assertTrue(admin_user.is_staff)
		self.assertTrue(admin_user.is_superuser)


class DriveBaseTest(TestCase):
	def setUp(self):
		self.factory = RequestFactory()
		self.user = User.objects.create_user(
			username="testuser", password="test.pass"
		)
		self.client.login(username="testuser", password="test.pass")

	@login_required
	def test_user_logged_in(self):
		assert self.user.is_authenticated

	@login_required
	def test_drive_home_url(self):
		response = self.client.get("/drive/")
		self.assertEqual(response.status_code, 200)

	def test_drive_home_title(self):
		response = self.client.get("/drive/")
		self.assertContains(response, "<title>My Drive</title>")

	def test_drive_home_template(self):
		response = self.client.get("/drive/")
		self.assertTemplateUsed(response, "drive_data/drive_home.html")

	def test_drive_home_view(self):
		request = self.factory.get("/drive")
		request.user = self.user
		response = DriveDataView.as_view()(request)
		self.assertEqual(response.status_code, 200)
#
# ## TODO
# # @staticmethod
#
#
# def get_image_file(name="test.png", ext='png', size=(50, 50), color=(120, 120, 120)):
# 	file_obj = BytesIO()
# 	image = Image.new("RGBA", size=size, color=color)
# 	image.save(file_obj, ext)
# 	file_obj.seek(0)
# 	return File(file_obj, name=name)

#
# # https://stackoverflow.com/questions/26298821/django-testing-model-with-imagefield
# class DriveFileUpload(TestCase):
#
# 	def setUp(self):
# 		self.user = User.objects.create_user(
# 			username="testuser", password="test.pass"
# 		)
# 		self.client.login(username="testuser", password="test.pass")
# 		self.user.save()
#
# 	def test_upload_file(self):
# 		request = self.client.get("/drive/upload/?next=/drive")
# 		f = get_image_file()
# 		# response = self.client.get("/drive/upload", f)
# 		response = file_upload_view(request, f)
# 		self.assertEqual(response.status_code, 200)
