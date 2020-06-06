from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.conf import settings
from registration import views

urlpatterns = [
    path('', views.index_view, name='home'),
    path('dashboard/', views.dashboard_view, name="dashboard"),
    path('login/', LoginView.as_view(), name="login_url"),
    path('register/', views.register_view, name="register_url"),
    path(
        'verify/<uid>/<token>',
        views.verify_account,
        name="account_verification",
    ),
    path(
        'logout/',
        LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL),
        name="logout",
    ),
]
