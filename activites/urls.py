from django.contrib import admin
from django.urls import path

from activites.views import show_activity

urlpatterns = [
    path("show_activities/", show_activity),
]
