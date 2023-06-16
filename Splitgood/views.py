from io import BytesIO

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.views import View
from django.views.decorators.csrf import csrf_protect

from group.models import Group
from userprofile.models import Profile


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
        profile = Profile()
        profile.user = user
        profile.save()

    return render(request, "home.html")


def dashboard(request):
    groups = Group.objects.filter(users=request.user.id)
    paginator = Paginator(groups, 6)  # Create a Paginator instance with 6 items per page
    page_number = request.GET.get('page', 1)  # Get the current page number from the request's query parameters
    page_obj = paginator.get_page(page_number)  # Get the Page object for the current page number
    context = {'page_obj': page_obj}
    return render(request, "dashboard.html", context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return redirect('registration')
        login(request, user)
        groups = Group.objects.filter(users=request.user.id)
        paginator = Paginator(groups, 6)  # Create a Paginator instance with 6 items per page
        page_number = request.GET.get('page', 1)  # Get the current page number from the request's query parameters
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}

        return render(request, "dashboard.html", context)


def logout_view(request):
    logout(request)
    return render(request, "home.html")


class InvitedRegisterView(View):

    def get(self, request):
        uuid = request.POST.get('uuid')
        group = Group.objects.get(uuid=uuid)
        group_name = group.group_name
        context = {'group_name': group_name, 'uuid': uuid}
        return render(request, 'invited_register.html', context)

    def post(self, request, uuid=None):
        group = Group.objects.get(uuid=uuid)
        group_name = group.group_name
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
        context = {'groups': groups, 'group_name': group_name}
        return render(request, "dashboard.html", context)
