from django.shortcuts import render
import requests


# Create your views here.

def team_view(request):
    return render(request, "team/team.html")
