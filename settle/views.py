from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.shortcuts import render
import razorpay
from django.views.decorators.csrf import csrf_exempt

from group.models import Group
from django.shortcuts import render

from split.models import Expense, Borrower, Lender

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def settle_view_group(request):
    groups = Group.objects.filter(users=request.user)

    return render(request, 'settle_expense_group.html', context={'groups': groups})


def settle_view(request):
    group = request.GET.get('group_id')
    amount = []
    lender = []
    lender_id = []
    expense = list(Expense.objects.filter(Q(group=group) & Q(users=request.user)).values_list('id', flat=True))
    borrower = list(
        Borrower.objects.filter(Q(expense__in=expense) & Q(borrowers=request.user.id) & Q(is_paid=False)).values(
            'lender').annotate(
            total=Sum('borrows')).order_by().values_list('lender__lender__username', 'total', 'lender_id'))

    for item in borrower:
        lender.append(item[0])
        amount.append(item[1])
        lender_id.append(item[2])
    borrow_list = zip(lender, amount, lender_id)
    length = len(lender_id)
    context = {'borrow_list': borrow_list, 'group': group, 'length': length}
    return render(request, 'settle_up.html', context)


def process_settle(request):
    lender_id = request.GET.get('id')
    amount = request.GET.get('amount')
    group = request.GET.get('group')
    context = {'lender_id': lender_id, 'amount': amount, 'group': group}

    return render(request, 'payments.html', context)


def process_payment(request):
    payment_method = request.POST.get('payment-method')
    if payment_method == 'online':
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

        return render(request, 'payment_online.html', context=context)
    else:
        lender_id = request.POST.get('lender_id')
        group = request.POST.get('group')
        borrow_transaction = Borrower.objects.filter(
            Q(borrowers=request.user.id) & Q(lender=lender_id) & Q(is_paid=False) & Q(group=group))
        for i in borrow_transaction:
            i.is_paid = True
            i.save()
        return render(request, 'dashboard.html')


@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":

        # get the required parameters from post request.
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        # verify the payment signature.
        result = razorpay_client.utility.verify_payment_signature(
            params_dict)
        if result is not None:
            # amount =   # Rs. 200
            # amount =

            # capture the payemt
            # razorpay_client.payment.capture(payment_id)

            # render success page on successful caputre of payment

            return render(request, 'dashboard.html')
        else:

            # if there is an error while capturing payment.
            return render(request, 'paymentfail.html')
    else:

        # if signature verification fails.
        return render(request, 'paymentfail.html')
