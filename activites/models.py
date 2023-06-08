from _ast import Delete

from django.db import models
from django.contrib.auth.models import User

from group.models import Group
from split.models import Expense


# Create your models here.
class Activities(models.Model):
    Deleted = "DE"
    Added = "AD"
    Paid = "PD"
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, null=True)
    activity = models.CharField(max_length=10)
    amount = models.IntegerField(blank=True, null=True)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
