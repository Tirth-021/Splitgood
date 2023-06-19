from django.contrib.auth.models import User
from django.db import models
from phone_field import PhoneField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, upload_to='profile_image')
    mobile_number = PhoneField(blank=True, help_text='Contact phone number')

