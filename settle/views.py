from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.shortcuts import render

from group.models import Group
from django.shortcuts import render

from split.models import Expense, Borrower, Lender


def settle_view_group(request):
    groups = Group.objects.filter(users=request.user)
    print(groups)
    return render(request, 'settle_expense_group.html', context={'groups': groups})


def settle_view(request):
    group = request.GET.get('group_id')
    amount = []
    lender = []
    expense = list(Expense.objects.filter(Q(group=group) & Q(users=request.user)).values_list('id', flat=True))
    borrower = list(
        Borrower.objects.filter(Q(expense__in=expense) & Q(borrowers=request.user.id)).values('lender').annotate(
            total=Sum('borrows')).order_by().values_list('lender__lender__username', 'total'))

    group_name = Group.objects.filter(id=group)[0]

    for item in borrower:
        lender.append(item[0])
        amount.append(item[1])
    borrow_list = zip(lender, amount)
    context = {'borrow_list': borrow_list}
    return render(request, 'settle_up.html', context)
