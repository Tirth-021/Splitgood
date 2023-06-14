from io import BytesIO

from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import logout, authenticate, login
from group.models import Group


def home(request):
    return render(request, "home.html")


def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = User.objects.create_user(username)
        user.set_password(password)
        user.email = email
        user.save()

    return render(request, "home.html")


def dashboard(request):
    groups = Group.objects.filter(users=request.user.id)
    context = {'groups': groups}
    return render(request, "dashboard.html", context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        login(request, user)
    groups = Group.objects.filter(users=request.user.id)
    context = {'groups': groups}

    return render(request, "dashboard.html", context)


def logout_view(request):
    logout(request)
    return render(request, "home.html")


def invited_register(request, uuid):
    group = Group.objects.get(uuid=uuid)
    group_name = group.group_name
    context = {'group_name': group_name,'uuid':uuid}
    return render(request, 'invited_register.html', context)


def add_registered(request):
    uuid = request.POST.get('uuid')
    group = Group.objects.get(uuid=uuid)
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    user = User.objects.create_user(username)
    user.set_password(password)
    user.email = email
    user.save()
    login(request, user)
    group.users.add(user)
    groups = Group.objects.filter(users=request.user.id)
    context = {'groups': groups}
    return render(request, "dashboard.html", context)