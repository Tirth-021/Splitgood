from django.urls import path

from group.views import group_view, create_group, show_group, invite_users, send_invite

urlpatterns = [
    path("group_view/", group_view),
    path("create_group/", create_group),
    path("show_group/", show_group),
    path("invite_user/", invite_users),
    path("send_invite/", send_invite),
]
