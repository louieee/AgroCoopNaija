from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class User(AbstractUser):
    gender_choice = (('M', 'Male'), ('F', 'Female'))
    is_cooperative_member = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    image = models.ImageField(upload_to='image/', default='/')
    phone_no = models.CharField(max_length=20, blank=True)
    specialization = models.CharField(max_length=255, default='')
    location = models.CharField(max_length=20, default='')
    bank = models.CharField(max_length=255, blank=True)
    account_name = models.CharField(max_length=255, default="", blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=1, choices=gender_choice, default='M')
    date_of_birth = models.DateField(default=now)

    def user_age(self):
        return now().year - self.date_of_birth.year
