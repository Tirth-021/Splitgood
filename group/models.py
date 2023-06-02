from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


# Create your models here.

class Group(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_grp_created_by')
    group_name = models.CharField(max_length=30)
    group_description = models.TextField()
    users = models.ManyToManyField(User, related_name='group')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'group'
