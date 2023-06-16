from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core import mail
from django.db.models import Q
from django.shortcuts import render
from django.views import View

from Splitgood import settings
from activites.models import Activities
from group.models import Group


class CreateGroupView(LoginRequiredMixin, View):
    login_url = 'login/'

    def get(self, request):
        users = User.objects.exclude(Q(username=request.user.username) | Q(is_superuser=True))
        return render(request, 'add_group.html', context={'users': users})

    def post(self, request):
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
            activity = Activities()
            activity.activity = "Added User"
            activity.group_id = group.id
            activity.user_id = request.user.id
            activity.added = user[0]
            activity.save()
        group.users.add(request.user)
        group.save()

        return render(request, 'dashboard.html')


@login_required(login_url='login/')
def show_group(request):
    group_id = request.GET.get('id')
    group = Group.objects.filter(id=group_id)[0]
    activity = Activities.objects.filter(group=group).values("activity", "amount", "expense__expense_name",
                                                             "group__group_name", "user__username", "date",
                                                             "paid_to__lender__username",
                                                             "added_id__username").order_by("-date")
    context = {'activity': activity, 'group_id': group_id}
    return render(request, 'group_view.html', context)


class InviteUsersView(LoginRequiredMixin, View):
    template_name = 'invite-users.html'

    def get(self, request):
        group_id = request.GET.get('group_id')
        group = Group.objects.filter(id=group_id).first()
        group_id = group.id
        group_name = group.group_name
        g_users = list(group.users.all().values_list('id', flat=True))
        left_users = User.objects.exclude(Q(id__in=g_users) | Q(is_superuser=True))
        uuid = group.uuid
        context = {'group_id': group_id, 'name': group_name, 'uuid': uuid, 'users': left_users}
        return render(request, self.template_name, context)

    def post(self, request):
        uuid = request.POST.get('uuid')
        names = request.POST.getlist('users_email')
        group_id = request.POST.get('group_id')
        group = Group.objects.filter(id=group_id).first()
        group_name = group.group_name
        users = list(User.objects.all().values_list("username"))

        for i in names:
            if i in users:
                user = User.objects.filter(username=i).first()
                group.users.add(user)
            else:
                send_email(i, uuid, group_name)

        groups = Group.objects.filter(users=request.user.id)
        context = {'groups': groups}
        return render(request, 'dashboard.html', context)


def send_email(email, uuid, group_name):
    uri = f"http://127.0.0.1:8000/invited-register/{uuid}"
    connection = mail.get_connection()
    subject = "Welcome to Split-good "
    message = "We are glad to have you here! \n" \
              "You are invited to join " \
              + group_name + "\nYou can signup on " + uri
    email = mail.EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        connection=connection,
    )
    email.send()
