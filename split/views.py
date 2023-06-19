from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from activites.models import Activities
from group.models import Group
from split.models import Expense
from split.utils.utils import split, edit_expense



def add_expense(request):
    group_info = Group.objects.filter(users=request.user)

    return render(request, 'add_group_expense.html', context={'group_info': group_info})


class ExpenseView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'add_expense.html'

    def get(self, request):
        group_id = request.GET.get('group_id')
        group = Group.objects.filter(id=group_id)
        ids = group[0].users.all().values('id')
        return render(request, self.template_name,
                      context={'group_id': group_id, 'group': group[0], 'users': group[0].users.all(), 'ids': ids})

    def post(self, request):
        context = split(request)
        return render(request, 'list_expenses.html', context)


class EditExpenseView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'add_expense.html'

    def get(self, request):
        expense_id = request.GET.get('expense')

        expense = Expense.objects.filter(id=expense_id)[0]

        expense_name = expense.expense_name

        date = expense.created_at.date().strftime("%Y-%m-%d")

        amount = expense.amount

        group_rec = expense.group_id
        group_id = Group.objects.filter(id=group_rec)[0]
        members = group_id.users.all()
        context = {'expense_name': expense_name, 'expense': expense, 'amount': amount, 'group': group_rec,
                   'users': members,
                   'group_id': group_id, 'date': date, 'expense_id': expense_id}
        return render(request, 'edit_expense.html', context)

    def post(self, request):
        context = edit_expense(request)
        return render(request, 'list_expenses.html', context)



def delete_expense(request):
    expense_id = request.POST.get('expense_id')
    group = request.POST.get('group')
    g = Group.objects.get(id=group)
    expense = Expense.objects.get(id=expense_id)
    if expense.expense_by == request.user.id:
        expense.is_deleted = True
        expense.save()
        activity = Activities()
        activity.group = g
        activity.user = request.user
        activity.expense = expense
        activity.activity = "Deleted Expense"
        activity.save()
        return render(request, 'list_expenses.html')
