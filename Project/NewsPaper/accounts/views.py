from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from posts.models import Author
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from allauth.account.views import SignupView
from .forms import CommonSignupForm

@login_required
def upgrade_me(request):
    user = request.user
    Author.objects.create(user=request.user)
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/posts')
