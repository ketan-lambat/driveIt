from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from .views import index_view


class RegistrationPageTest(TestCase):

	def test_root_url(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)

	def test_root_url_resolves_to_home_page(self):
		found_url = resolve('/')
		self.assertEqual(found_url.func, index_view)

	def test_root_title(self):
		response = self.client.get('/')
		self.assertContains(response, "<title>Simple Auth System</title>")
		self.assertTemplateUsed(response, "registration/index.html")

