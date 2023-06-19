from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
import razorpay
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from group.models import Group
from django.shortcuts import render
from settle.utils.utils import online_pay, cash_transaction
from split.models import Expense, Borrower

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def settle_view_group(request):
    groups = Group.objects.filter(users=request.user)

    return render(request, 'settle_expense_group.html', context={'groups': groups})


class SettleView(View):
    template_name = 'settle_up.html'

    def get(self, request):
        group = request.GET.get('group_id')
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
        context = {'borrow_list': borrow_list, 'group': group, 'length': length}
        return render(request, self.template_name, context)

    def post(self, request):
        lender_id = request.POST.get('id')
        amount = request.POST.get('amount')
        group = request.POST.get('group')
        context = {'lender_id': lender_id, 'amount': amount, 'group': group}
        return render(request, 'payments.html', context)


def process_payment(request):
    payment_method = request.POST.get('payment-method')
    if payment_method == 'online':
        context = online_pay(request)
        return render(request, 'payment_online.html', context=context)
    else:
        cash_transaction(request)
        groups = Group.objects.filter(users=request.user.id)
        paginator = Paginator(groups, 6)  # Create a Paginator instance with 6 items per page
        page_number = request.GET.get('page', 1)  # Get the current page number from the request's query parameters
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}
        return render(request, 'dashboard.html', context)


@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":

        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        result = razorpay_client.utility.verify_payment_signature(
            params_dict)
        if result is not None:
            messages.success(request, "You are settled up.")
            return render(request, 'dashboard.html')
        else:

            # if there is an error while capturing payment.
            return render(request, 'paymentfail.html')
    else:

        # if signature verification fails.
        return render(request, 'paymentfail.html')
