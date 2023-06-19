from django.contrib.auth.decorators import login_required
from django.urls import path

from userprofile.views import UserView

urlpatterns = [
    path('user_profile/', login_required(UserView.as_view(), login_url='/'), name='user_profile'),
]
