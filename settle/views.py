from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render

from group.models import Group
from django.shortcuts import render


# Create your views here.
def settle_view(request):
    group = Group.objects.filter(users=request.user.id).values_list('id',flat=True)
    breakpoint()
    expense = Expense.objects.filter(group_id in group)

    return render(request, 'settle_up.html')
