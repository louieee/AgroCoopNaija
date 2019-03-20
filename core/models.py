from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_cooperative_member = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/')
    phone_no = models.CharField(max_length=20, blank=True)


class Tag(models.Model):
    name = models.CharField(max_length=255, primary_key=True)


