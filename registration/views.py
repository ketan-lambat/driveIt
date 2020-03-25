from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from .forms import CreateUserForm


def index_view(request):
	return render(request, 'registration/index.html')


@login_required
def dashboard_view(request):
	return render(request, 'registration/dashboard.html')


def register_view(request):
	if request.method == "POST":
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login_url')
	else:
		form = CreateUserForm()

	return render(request, 'registration/register.html', {'form': form})


def login_view(request):
	if request.method == 'POST':
		try:
			username, password = request.POST.get('username'), request.POST.get('password')
		except:
			return HttpResponseBadRequest()
		user = authenticate(request, username=username, password=password)
		if not user:
			return HttpResponse('Unable to login.')
		auth_login(request, user)
		return redirect('dashboard')
