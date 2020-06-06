from django.test import TestCase
from django.urls import resolve
from .models import User
from .views import index_view, dashboard_view


class UserLoggedInTest(TestCase):
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


class DashboardPageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="test.pass"
        )
        self.response = self.client.login(
            username="testuser", password="test.pass"
        )

    def test_user_logged_in(self):
        assert self.user.is_authenticated

    def test_root_url(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_root_url_view(self):
        dashboard_url = resolve("/")
        self.assertEqual(dashboard_url.func, index_view)

    def test_root_title(self):
        response = self.client.get("/")
        self.assertContains(response, "<title>TDrive</title>")

    def test_root_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "registration/index.html")


class LoginPageTest(TestCase):
    def test_login_url(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_root_title(self):
        response = self.client.get("/login/")
        self.assertContains(response, "<title>Login | TDrive</title>")
