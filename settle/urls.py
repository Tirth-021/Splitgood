from django.urls import path

from settle.views import settle_view_group, process_payment, paymenthandler, SettleView

urlpatterns = [
    path("view_settle/", settle_view_group),
    path("process_settle/", SettleView.as_view()),
    path("process_payment/", process_payment),
    path('process_payment/paymenthandler/', paymenthandler),

]
