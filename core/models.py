from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_cooperative_member = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/')
    phone_no = models.CharField(max_length=20, blank=True)


class Tag:
    tags = ['fishery', 'animal husbandry', 'piggery', 'horticulture', 'banana farming']


class Bank:
    bank = ['First Bank of Nigeria', 'Stanbic IBTC', 'GTB bank', 'Access Bank', 'Oceanic Bank']
