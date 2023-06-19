from django.contrib.auth.decorators import login_required
from django.urls import path

from activites.views import show_activity

urlpatterns = [
    path("show_activities/", login_required(show_activity, login_url='/')),
]
