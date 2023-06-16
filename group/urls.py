from django.urls import path

from group.views import show_group, CreateGroupView, InviteUsersView

urlpatterns = [
    path("create_group/", CreateGroupView.as_view()),
    path("show_group/", show_group),
    path("invite_user/", InviteUsersView.as_view()),
]
