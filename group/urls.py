from django.contrib.auth.decorators import login_required
from django.urls import path

from group.views import show_group, CreateGroupView, InviteUsersView, activate_sd

urlpatterns = [
    path("create_group/", login_required(CreateGroupView.as_view(), login_url='/')),
    path("show_group/", login_required(show_group, login_url='/')),
    path("invite_user/", login_required(InviteUsersView.as_view(), login_url='/')),
    path("simply/", login_required(activate_sd, login_url='/')),
]
