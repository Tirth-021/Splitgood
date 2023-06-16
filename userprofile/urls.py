from django.urls import path

from userprofile.views import UserView

urlpatterns = [
    path('user_profile/', UserView.as_view(), name='user_profile'),
]
