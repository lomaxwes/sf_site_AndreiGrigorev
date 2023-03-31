from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import upgrade_me

# from .views import welcome

app_name = 'accounts'

urlpatterns = [
    path('upgrade/', upgrade_me, name='upgrade'),
    # path('welcome/', welcome, name='welcome'),
]