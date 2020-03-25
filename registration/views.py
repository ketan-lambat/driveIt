from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode as b64_encode, urlsafe_base64_decode as b64_decode

from mail import send_mail
from .forms import UserRegistrationForm
from .models import User
from .tokens import registration_token_generator


def index_view(request):
    return render(request, 'registration/index.html')


@login_required
def dashboard_view(request):
    return render(request, 'registration/dashboard.html')


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            u = form.save()
            user_token = registration_token_generator.make_token(u)
            b64id = b64_encode(bytes(str(u.pk).encode()))
            url = settings.URL + reverse('account_verification', args=[b64id, user_token])
            text = "Dear User,\n" + \
                   "Please open the link given below to verify your email for DriveIt account. \n" + url + \
                   "\nIf you did not request registration for DriveIt then please ignore this email."
            send_mail("Email Verification for DriveIt", text, text, [u.email])
            messages.info(request, "Account Activation link mailed.", fail_silently=True)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def verify_account(request, uid, user_token):
    pk = b64_decode(uid).decode()
    u = User.objects.get_or_none(pk=pk)
    if u is None or u.is_active:
        return HttpResponseBadRequest()
    elif not registration_token_generator.check_token(u, user_token):
        return HttpResponseBadRequest()
    else:
        u.is_active = True
        u.save()
        messages.info(request, "Account Verified", fail_silently=True)
        return redirect('login_url')


def login_view(request):
    if request.method == 'POST':
        try:
            username, password = request.POST.get('username'), request.POST.get('password')
        except KeyError:
            return HttpResponseBadRequest()
        user = authenticate(request, username=username, password=password)
        if not user:
            return HttpResponse('Unable to login.')
        auth_login(request, user)
        return redirect('dashboard')
