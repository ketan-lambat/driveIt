from django.test import TestCase, RequestFactory
from django.urls import resolve
from django.contrib.auth.decorators import login_required
from .views import *
from registration.models import User


# Create your tests here.

class BlogHomePageTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", password="test.pass"
        )
        self.client.login(username="testuser", password="test.pass")

    @login_required
    def test_blog_url(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_blog_view(self):
        blog_url = resolve('/blog/')
        self.assertEqual(blog_url.func, home)

    def test_blog_template(self):
        response = self.client.get("/blog/")
        self.assertTemplateUsed(response, "blog/home.html")

    def test_blog_title(self):
        response = self.client.get("/blog/")
        self.assertContains(response, "<title>blog|tdrive</title>")


class BlogPostFormTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", password="test.pass"
        )
        self.client.login(username="testuser", password="test.pass")

    def test_blogpost_template(self):
        response = self.client.get("/blog/post/form/")
        self.assertTemplateUsed(response, "blog/post_form.html")

class BlogMyPostTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", password="test.pass"
        )
        self.client.login(username="testuser", password="test.pass")

    def test_blogmypost_template(self):
        response = self.client.get("/blog/my-posts")
        self.assertTemplateUsed(response, "blog/my_posts.html")