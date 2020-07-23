from base import views
from django.urls import path
from django.urls import path, include, re_path

urlpatterns = [
    path("team/", views.team_view, name="team"),
]
