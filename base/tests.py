from django.test import TestCase
from django.urls import resolve
from .views import team_view


# Create your tests here.


class OurTeamPageTest(TestCase):
    def test_teampage_url(self):
        response = self.client.get('/base/team/')
        self.assertEqual(response.status_code, 200)

    def test_teampage_view(self):
        team_url = resolve('/base/team/')
        self.assertEqual(team_url.func, team_view)

    def test_teampage_template(self):
        response = self.client.get("/base/team/")
        self.assertTemplateUsed(response, "team/team.html")
