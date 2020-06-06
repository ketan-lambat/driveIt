from django.test import TestCase
from django.urls import resolve, reverse
from django.views import generic
from registration.models import User
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
        self.user = User.objects.create_user(
            username="testuser", password="test.pass"
        )
        self.client.login(username="testuser", password="test.pass")

    def test_user_logged_in(self):
        assert self.user.is_authenticated

    def test_drive_home_url(self):
        response = self.client.get('/drive/')
        self.assertEqual(response.status_code, 200)

    ### *** TODO ***
    # def test_drive_home_url_view(self):
    # 	drive_home_url = resolve('/drive/')
    # 	self.assertEqual(drive_home_url.func, DriveDataView.as_view())

    def test_drive_home_title(self):
        response = self.client.get('/drive/')
        self.assertContains(response, "<title>My Drive</title>")

    def test_drive_home_template(self):
        response = self.client.get('/drive/')
        self.assertTemplateUsed(response, "drive_data/drive_home.html")
