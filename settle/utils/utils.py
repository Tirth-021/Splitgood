import heapq
from collections import defaultdict

import networkx as nx
import razorpay
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, Sum, Value
from django.db.models.functions import Coalesce

from Splitgood import settings
from activites.models import Activities
from group.models import Group
from split.models import Borrower, Lender, Expense


def unsimplify(request, group):
    amount = []
    lender = []
    lender_id = []
    expense = list(
        Expense.live_expense.filter(Q(group=group) & Q(users=request.user) & Q(is_deleted=False)).values_list('id',
                                                                                                              flat=True))
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
    return {'borrow_list': borrow_list, 'group': group, 'length': length}


def simplify(request, g):
    net_amounts = defaultdict(int)  # {user: net_amount}
    for lender in Lender.objects.filter(expense__group=g):
        net_amounts[lender.lender] += lender.lends
        for borrower in Borrower.objects.filter(lender__id=lender.id):
            net_amounts[borrower.borrowers] -= borrower.borrows

    # Step 2: Separate debtors and creditors
    debtors = []  # [(amount, user)]
    creditors = []  # [(amount, user)]
    for user, amount in net_amounts.items():
        if amount < 0:
            heapq.heappush(debtors, (-amount, user))
        elif amount > 0:
            heapq.heappush(creditors, (-amount, user))  # Use negative amounts to get a max heap
    # Step 3: Match debtors and creditors
    transactions = []  # [(debtor, creditor, amount)]
    while debtors and creditors:
        debtor_amount, debtor_user = heapq.heappop(debtors)
        creditor_amount, creditor_user = heapq.heappop(creditors)
        transaction_amount = min(debtor_amount, -creditor_amount)

        transactions.append((debtor_user, creditor_user, transaction_amount))

        if -debtor_amount + transaction_amount < 0:
            heapq.heappush(debtors, (debtor_amount + transaction_amount, debtor_user))
        if -creditor_amount - transaction_amount > 0:
            heapq.heappush(creditors, (creditor_amount + transaction_amount, creditor_user))

    return transactions


def online_pay(request):
    razorpay_client = razorpay.Client(
        auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
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
