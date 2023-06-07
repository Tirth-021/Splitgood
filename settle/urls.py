from django.contrib import admin
from django.urls import path

from settle.views import settle_view, settle_view_group, process_settle, process_payment, paymenthandler

urlpatterns = [
    path("view_settle/", settle_view_group),
    path("transactions/", settle_view),
    path("process_settle/", process_settle),
    path("process_payment/", process_payment),
    path('process_payment/paymenthandler/', paymenthandler),


]