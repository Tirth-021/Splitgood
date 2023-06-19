from django.contrib.auth.decorators import login_required
from django.urls import path

from settle.views import settle_view_group, process_payment, paymenthandler, SettleView

urlpatterns = [
    path("view_settle/", login_required(settle_view_group, login_url='/')),
    path("process_settle/", login_required(SettleView.as_view(), login_url='/')),
    path("process_payment/", login_required(process_payment, login_url='/')),
    path('process_payment/paymenthandler/', paymenthandler),

]
