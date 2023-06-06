from django.contrib import admin
from django.urls import path

from settle.views import settle_view

urlpatterns = [
    path("view_settle/", settle_view),

]