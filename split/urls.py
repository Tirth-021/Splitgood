from django.contrib.auth.decorators import login_required
from django.urls import path

from split.views import add_expense, ExpenseView, EditExpenseView

urlpatterns = [
    path("add_expense/", login_required(add_expense, login_url='/')),
    path("split_expense/", login_required(ExpenseView.as_view(), login_url='/')),
    path("edit_expense/", login_required(EditExpenseView.as_view(), login_url='/')),
]
