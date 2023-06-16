from django.urls import path

from split.views import add_expense, edit_page, edit_expense, ExpenseView

urlpatterns = [
    path("add_expense/", add_expense),
    path("split_expense/", ExpenseView.as_view()),
    path("edit_expense/", edit_page),
    path("process_edit/", edit_expense),
]
