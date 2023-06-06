from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render

from group.models import Group


def group_view(request):
    users = User.objects.exclude(Q(username=request.user.username) | Q(is_superuser=True))

    data = {'users': users}
    return render(request, 'add_group.html', context={'users': users})


def create_group(request):
    group_name = request.POST.get('group_name')
    description = request.POST.get('group_desc')
    users_lst = request.POST.getlist('users')
    users = []
    for i in users_lst:
        users.append(User.objects.filter(username=i))


    group = Group()
    group.created_by = request.user
    group.group_name = group_name
    group.group_description = description
    group.save()
    for user in users:
        group.users.add(user[0])
    group.users.add(request.user)
    group.save()
    return render(request, 'dashboard.html')
