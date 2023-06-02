from django.contrib import admin
from django.urls import path

from group.views import group_view, create_group

urlpatterns = [
    path("group_view/", group_view),
    path("create_group/", create_group),
]
