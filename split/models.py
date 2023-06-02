from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE

from group.models import Group


# Create your models here.

class Expense(models.Model):
    expense_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_created_by')
    expense_name = models.CharField(max_length=30)
    amount = models.IntegerField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'expense'


class Lender(models.Model):

    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    lender = models.ForeignKey(User, on_delete=models.CASCADE)
    lends = models.IntegerField()
    expense_name = models.CharField(max_length=30, default="")


class Borrower(models.Model):
    borrowers = models.ManyToManyField(User)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    lender = models.ForeignKey(Lender, on_delete=models.CASCADE)
    borrows = models.IntegerField()
    expense_name = models.CharField(max_length=30, default="")
