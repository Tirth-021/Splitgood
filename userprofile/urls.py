from django.urls import path

from userprofile.views import user_profile, updateuser

urlpatterns = [
    path("user_profile/", user_profile),
    path("updateuser/",updateuser),
]