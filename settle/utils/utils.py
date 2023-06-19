from django.contrib import messages
from django.db.models import Q

from Splitgood import settings
from activites.models import Activities
from group.models import Group
from settle.views import razorpay_client
from split.models import Borrower


def online_pay(request):
    lender_id = request.POST.get('lender_id')
    amount = request.POST.get('amount')
    group = request.POST.get('group')
    final_amount = int(amount) * 100

    currency = 'INR'
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=final_amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': final_amount,
        'currency': currency,
        'callback_url': callback_url,
    }

    borrow_transaction = Borrower.objects.filter(
        Q(borrowers=request.user.id) & Q(lender=lender_id) & Q(is_paid=False) & Q(group=group))
    for i in borrow_transaction:
        i.is_paid = True
        i.save()
    activity = Activities()
    activity.activity = "Paid"
    activity.amount = int(amount)
    g = Group.objects.get(group=group)
    activity.group = g
    activity.user = request.user
    activity.save()
    return context

def cash_transaction(request):
    lender_id = request.POST.get('lender_id')
    group = request.POST.get('group')
    amount = request.POST.get('amount')
    borrow_transaction = Borrower.objects.filter(
        Q(borrowers=request.user.id) & Q(lender=lender_id) & Q(is_paid=False) & Q(group=group))
    for i in borrow_transaction:
        i.is_paid = True
        i.save()
    activity = Activities()
    activity.activity = "Paid"
    activity.amount = int(amount)
    g = Group.objects.get(id=group)
    activity.group = g
    activity.user = request.user
    activity.paid_to = Lender.objects.filter(id=lender_id)[0]
    activity.save()
    messages.success(request, "You are settled up.")
