from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.utils.dateparse import parse_datetime

from group.models import Group
from split.models import Expense, Lender, Borrower




def add_expense(request):
    group_info = Group.objects.filter(users=request.user)

    return render(request, 'add_group_expense.html', context={'group_info': group_info})


def split_expense(request):
    group_id = request.GET.get('group_id')
    group = Group.objects.filter(id=group_id)
    ids = group[0].users.all().values('id')
    return render(request, 'add_expense.html',
                  context={'group_id': group_id, 'group': group[0], 'users': group[0].users.all(), 'ids': ids})


def process_expense(request):
    split_type = request.POST.get('split_type')
    expense_name = request.POST.get('expense_name')
    amount = request.POST.get('amount')
    group = request.POST.get('group_id')
    users_lst = request.POST.getlist('users_selected')
    uneuser = request.POST.getlist('une_users_selected')
    date = parse_datetime(request.POST.get('date'))
    g = Group.objects.filter(id=group)[0]
    r_user = request.POST.getlist('r_users_selected')

    member_list = []
    if len(r_user) > 0:
        for i in r_user:
            us = User.objects.get(username=i)

            member_list.append(us.id)
    if len(uneuser) > 0:
        for i in uneuser:
            us = User.objects.get(username=i)

            member_list.append(us.id)

    users = []
    uneusers = []
    r_users = []
    for i in users_lst:
        users.append(User.objects.filter(username=i))
    for i in uneuser:
        uneusers.append(User.objects.filter(username=i))
    for i in r_user:
        r_users.append(User.objects.filter(username=i))
    current_user = User.objects.filter(id=request.user.id)[0]
    expense = Expense()
    expense.expense_by = current_user
    expense.expense_name = expense_name
    expense.amount = amount
    expense.created_at = date
    expense.group = g
    expense.save()

    if split_type == 'split_equally':

        for user in users:
            expense.users.add(user[0])

        per_person_amount = int(amount) / (len(users))

        lender = Lender()
        lender.expense = expense
        lender.lender = User.objects.filter(id=request.user.id)[0]
        lender.lends = per_person_amount * (len(users) - 1)
        lender.expense_name = expense_name

        lender.save()

        for i in users_lst:
            borrower = Borrower()
            borrower.expense = expense
            borrower.borrowers = User.objects.filter(username=i)[0]
            borrower.lender = Lender.objects.filter(lender_id=request.user.id)[0]
            borrower.borrows = per_person_amount
            borrower.expense_name = expense_name
            borrower.group = g
            borrower.save()

        own_delete = Borrower.objects.get(Q(borrowers_id=request.user.id) & Q(expense=expense))
        own_delete.delete()

        context = {'expense_name': expense_name, 'date': date, 'lends': per_person_amount * (len(users) - 1),
                   'expense': expense}

        return render(request, 'list_expenses.html', context)

    if split_type == 'split_unequally':

        own_amount = request.POST.get('une_value_' + str(request.user.id))
        for user in uneusers:
            expense.users.add(user[0])

        lender = Lender()
        lender.expense = expense
        lender.lender = User.objects.filter(id=request.user.id)[0]
        lender.lends = int(amount) - int(own_amount)
        lender.expense_name = expense_name

        lender.save()
        for i in uneuser:
            borrower = Borrower()
            borrower.expense = expense
            borrower.borrowers = User.objects.filter(username=i)[0]
            borrower.lender = Lender.objects.filter(lender_id=request.user.id)[0]
            borrower.borrows = request.POST.get('une_value_' + str(member_list[i]))
            borrower.expense_name = expense_name
            borrower.group = g
            borrower.save()
        own_delete = Borrower.objects.get(Q(borrowers_id=request.user.id) & Q(expense=expense))
        own_delete.delete()

        context = {'expense_name': expense_name, 'date': date, 'lends': (int(amount) - int(own_amount)),
                   'expense': expense}

        return render(request, 'list_expenses.html', context)

    if split_type == 'split_ratio':

        own_amount = request.POST.get('une_r_value_' + str(request.user.id))
        for user in r_users:
            expense.users.add(user[0])

        lender = Lender()
        lender.expense = expense
        lender.lender = User.objects.filter(id=request.user.id)[0]
        lender.lends = int(amount) - int(own_amount)
        lender.expense_name = expense_name

        lender.save()
        for i in r_user:
            borrower = Borrower()
            borrower.expense = expense
            borrower.borrowers = User.objects.filter(username=i)[0]
            borrower.lender = Lender.objects.filter(lender_id=request.user.id)[0]
            borrower.borrows = request.POST.get('une_r_value_' + str(member_list[i]))
            borrower.expense_name = expense_name
            borrower.save()
        own_delete = Borrower.objects.get(Q(borrowers_id=request.user.id) & Q(expense=expense))
        own_delete.delete()

        context = {'expense_name': expense_name, 'date': date, 'lends': (int(amount) - int(own_amount)),
                   'expense': expense}

        return render(request, 'list_expenses.html', context)


def edit_page(request):
    expense_id = request.GET.get('expense')


    expense = Expense.objects.filter(id=expense_id)[0]

    expense_name = expense.expense_name

    date = expense.created_at.date().strftime("%Y-%m-%d")

    amount = expense.amount

    group_rec = expense.group_id
    group_id = Group.objects.filter(id=group_rec)[0]
    members = group_id.users.all()
    context = {'expense_name': expense_name, 'expense': expense, 'amount': amount, 'group': group_rec, 'users': members,
               'group_id': group_id, 'date': date, 'expense_id': expense_id}
    return render(request, 'edit_expense.html', context)


def edit_expense(request):
    split_type = request.POST.get('split_type')
    expense_id = request.POST.get('expense_id')
    expense_name = request.POST.get('expense_name')
    amount = request.POST.get('amount')
    group = request.POST.get('group_id')
    users_lst = request.POST.getlist('users_selected')
    uneuser = request.POST.getlist('une_users_selected')
    date = parse_datetime(request.POST.get('date'))
    g = Group.objects.filter(id=group)[0]
    r_user = request.POST.getlist('r_users_selected')
    member_list = []
    user_list = []
    prev_users = Borrower.objects.filter(expense_id=expense_id)

    if len(users_lst) > 0:
        for i in users_lst:
            us = User.objects.get(username=i)
            member_list.append(us.id)
        for j in prev_users:
            prev_username = User.objects.get(id=j.borrowers_id).username
            user_list.append(prev_username)

    if len(r_user) > 0:
        for i in r_user:
            us = User.objects.get(username=i)
            member_list.append(us.id)
        for j in prev_users:
            prev_username = User.objects.get(id=j.borrowers_id).username
            user_list.append(prev_username)
    if len(uneuser) > 0:
        for i in uneuser:
            us = User.objects.get(username=i)
            member_list.append(us.id)
        for j in prev_users:
            prev_username = User.objects.get(id=j.borrowers_id).username
            user_list.append(prev_username)

    users = []
    uneusers = []
    r_users = []
    for i in users_lst:
        users.append(User.objects.filter(username=i))
    for i in uneuser:
        uneusers.append(User.objects.filter(username=i))
    for i in r_user:
        r_users.append(User.objects.filter(username=i))
    current_user = User.objects.filter(id=request.user.id)[0]
    username = str(current_user.username)

    expense = Expense.objects.get(id=expense_id)


    expense.expense_name = expense_name
    expense.amount = amount
    expense.created_at = date
    expense.save()

    if split_type == 'split_equally':

        for user in users:
            expense.users.add(user[0])

        per_person_amount = int(amount) / (len(users))

        lender = Lender.objects.filter(expense_id=expense_id)[0]
        lender.expense = expense
        lender.lends = per_person_amount * (len(users) - 1)
        lender.expense_name = expense_name

        lender.save()
        j = 0
        users_lst.remove(request.user.username)

        for i in users_lst:

            if i in user_list:
                borrower = Borrower.objects.filter(expense_id=expense_id)[j]
                borrower.expense = expense
                borrower.borrowers = User.objects.filter(username=i)[0]
                borrower.lender = Lender.objects.filter(lender_id=request.user.id)[0]
                borrower.borrows = per_person_amount
                borrower.expense_name = expense_name
                borrower.save()
            else:
                borrower = Borrower()
                borrower.expense = expense
                borrower.borrowers = User.objects.filter(username=i)[0]
                borrower.lender = Lender.objects.filter(lender_id=request.user.id)[0]
                borrower.borrows = per_person_amount
                borrower.expense_name = expense_name
                borrower.save()
            j = j + 1

        context = {'expense_name': expense_name, 'date': date, 'lends': per_person_amount * (len(users) - 1),
                   'expense': expense}

        return render(request, 'list_expenses.html', context)

    if split_type == 'split_unequally':

        own_amount = request.POST.get('une_value_' + str(request.user.id))
        for user in uneusers:
            expense.users.add(user[0])

        lender = Lender.objects.filter(expense_id=expense.id)[0]
        lender.expense = expense
        lender.lends = int(amount) - int(own_amount)
        lender.expense_name = expense_name

        lender.save()
        j = 0
        uneuser.remove(request.user.username)
        for i in uneuser:
            if i in user_list:
                borrower = Borrower.objects.filter(expense_id=expense_id)[j]
                borrower.expense = expense
                borrower.borrowers = User.objects.filter(username=i)[0]
                borrower.lender = Lender.objects.filter(lender_id=request.user.id)[0]
                borrower.borrows = request.POST.get('une_value_' + str(member_list[j]))
                borrower.expense_name = expense_name
                borrower.save()
            else:
                borrower = Borrower()
                borrower.expense = expense
                borrower.borrowers = User.objects.filter(username=i)[0]
                borrower.lender = Lender.objects.filter(lender_id=request.user.id)[0]
                borrower.borrows = request.POST.get('une_value_' + str(member_list[j]))
                borrower.expense_name = expense_name
                borrower.save()

            j = j + 1

        context = {'expense_name': expense_name, 'date': date, 'lends': (int(amount) - int(own_amount)),
                   'expense': expense}

        return render(request, 'list_expenses.html', context)

    if split_type == 'split_ratio':
        own_amount = request.POST.get('une_r_value_' + str(request.user.id))
        for user in r_users:
            expense.users.add(user[0])

        lender = Lender.objects.filter(expense_id=expense_id)[0]
        lender.expense = expense
        lender.lender = User.objects.filter(id=request.user.id)[0]
        lender.lends = int(amount) - int(own_amount)
        lender.expense_name = expense_name

        lender.save()
        j = 0
        r_user.remove(request.user.username)
        for i in r_user:
            if i in user_list:
                borrower = Borrower.objects.filter(expense_id=expense_id)[j]
                borrower.expense = expense
                borrower.borrowers = User.objects.filter(username=i)[0]
                borrower.lender = Lender.objects.filter(lender_id=request.user.id)[0]
                borrower.borrows = request.POST.get('une_r_value_' + str(member_list[j]))
                borrower.expense_name = expense_name
                borrower.save()
            else:
                borrower = Borrower()
                borrower.expense = expense
                borrower.borrowers = User.objects.filter(username=i)[0]
                borrower.lender = Lender.objects.filter(lender_id=request.user.id)[0]
                borrower.borrows = request.POST.get('une_r_value_' + str(member_list[j]))
                borrower.expense_name = expense_name
                borrower.save()

            j = j + 1

        context = {'expense_name': expense_name, 'date': date, 'lends': (int(amount) - int(own_amount)),
                   'expense': expense}

        return render(request, 'list_expenses.html', context)
