from django.urls import path

from split.views import add_expense, split_expense, process_expense, edit_page, edit_expense

urlpatterns = [
    path("add_expense/", add_expense),
    path("split_expense/", split_expense),
    path("process_expense/", process_expense),
    path("edit_expense/", edit_page),
    path("process_edit/", edit_expense),
]
