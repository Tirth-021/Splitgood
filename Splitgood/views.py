from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.views.decorators.cache import cache_control, never_cache


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def home(request):
    return render(request, "home.html")


def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = User.objects.create_user(username)
        user.set_password(password)
        user.email = email
        user.save()


    return render(request, "home.html")

def dashboard(request):
    return render(request, "dashboard.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        login(request, user)
    return render(request, "dashboard.html")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def logout_view(request):
    logout(request)
    return render(request, "home.html")
