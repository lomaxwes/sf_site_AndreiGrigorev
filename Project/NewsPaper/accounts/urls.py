from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from Project.NewsPaper.accounts.views import upgrade_me

app_name = 'accounts'

urlpatterns = [
    path('upgrade/', upgrade_me, name='upgrade'),
]