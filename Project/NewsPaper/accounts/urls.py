from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import upgrade_me

app_name = 'account'

urlpatterns = [
    path('upgrade/', upgrade_me, name='upgrade'),
]