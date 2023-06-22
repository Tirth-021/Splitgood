

import uuid as uuid
from django.contrib.auth.models import User
from django.db import models


class Group(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_grp_created_by')
    group_name = models.CharField(max_length=30)
    group_description = models.TextField()
    users = models.ManyToManyField(User, related_name='group')
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(unique=True, null=True, default=uuid.uuid4)
    is_simplified = models.BooleanField(default=False)

    class Meta:
        db_table = 'group'
