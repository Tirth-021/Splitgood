from django.contrib import admin
from django.urls import path

from settle.views import settle_view, settle_view_group

urlpatterns = [
    path("view_settle/", settle_view_group),
    path("transactions/", settle_view)

]