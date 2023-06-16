"""
URL configuration for Splitgood project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from .views import home, registration, login_view, logout_view, dashboard, InvitedRegisterView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home),
    path("home/", dashboard, name="home"),
    path("registration/", registration, name="registration"),
    path("login/", login_view),
    path("logout/", logout_view),
    path('invited-register/<uuid>/', InvitedRegisterView.as_view(), name='invited_register'),
    path('group/', include('group.urls')),
    path('split/', include('split.urls')),
    path('settle/', include('settle.urls')),
    path('activities/', include('activites.urls')),
    path('user/', include('userprofile.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
