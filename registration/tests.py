from django.contrib.auth import authenticate
from django.test import TestCase
from django.urls import resolve
from .models import User
from .views import index_view, dashboard_view
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required


class UserLoggedInTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username="testuser", password="test.pass"
		)
		self.user.save()

	def tearDown(self):
		self.user.delete()

	def test_correct(self):
		user = authenticate(username="testuser", password="test.pass")
		self.assertTrue((user is not None) and user.is_authenticated)

	def test_wrong_username(self):
		user = authenticate(username="user", password="test.pass")
		self.assertFalse((user is not None) and user.is_authenticated)

	def test_wrong_password(self):
		user = authenticate(username="testuser", password="pass")
		self.assertFalse((user is not None) and user.is_authenticated)

	def test_user_permission(self):
		self.assertFalse(self.user.is_superuser)
		self.assertTrue(self.user.is_active)
		self.assertFalse(self.user.is_staff)


class AdminLoggedInTest(TestCase):
	def setUp(self):
		self.admin = User.objects.create_superuser(
			username="admin", password="admin.pass"
		)
		self.admin.save()

	def teardown(self):
		self.admin.delete()

	def test_correct(self):
		admin = authenticate(username="admin", password="admin.pass")
		self.assertTrue((admin is not None) and admin.is_authenticated)

	def test_wrong_username(self):
		admin = authenticate(username="user", password="admin.pass")
		self.assertFalse((admin is not None) and admin.is_authenticated)

	def test_wrong_password(self):
		admin = authenticate(username="admin", password="pass")
		self.assertFalse((admin is not None) and admin.is_authenticated)

	def test_superuser_permission(self):
		self.assertTrue(self.admin.is_active)
		self.assertTrue(self.admin.is_staff)
		self.assertTrue(self.admin.is_superuser)


class DashboardPageTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username="testuser", password="test.pass"
		)
		self.response = self.client.login(
			username="testuser", password="test.pass"
		)

	@login_required
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

	def test_login_title(self):
		response = self.client.get("/login/")
		self.assertContains(response, "<title>Login | TDrive</title>")

	def test_login_template(self):
		response = self.client.get("/login/")
		self.assertTemplateUsed(response, "registration/login.html")


class UserLoggedOutTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username="testuser", password="test.pass"
		)
		self.response = self.client.login(
			username="testuser", password="test.pass"
		)

	def test_logout_url(self):
		response = self.client.get("/logout/?next=/")
		self.assertEqual(response['Location'], '/')
		self.assertEqual(response.status_code, 302)
