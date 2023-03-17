from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from ..posts.models import Author


@login_required
def upgrade_me(request):
    user = request.user
    Author.objects.create(user_id=request.user_id)
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/posts')