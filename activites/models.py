from django.db import models
from django.contrib.auth.models import User

from group.models import Group
from split.models import Expense, Lender


class Activities(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, null=True)
    activity = models.CharField(max_length=10)
    amount = models.IntegerField(blank=True, null=True)
    paid_to = models.ForeignKey(Lender, on_delete=models.CASCADE, related_name="paid_to", null=True)
    added = models.ForeignKey(User, on_delete=models.CASCADE, related_name="added", null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
