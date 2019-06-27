from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


def set_user_title(id_):
    user = User.objects.get(id=id_)
    if user.gender == 'Male':
        user.title = 'Mr'
    elif user.gender == 'Female':
        if user.marital_status != 'Married':
            user.title = 'Miss'
        else:
            user.title = 'Mrs'
    user.save()


class User(AbstractUser):
    is_cooperative_member = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    gender = models.CharField(max_length=7, default='Male')
    marital_status = models.CharField(max_length=50, default='Single')
    image = models.ImageField(upload_to='image/', default='/')
    show_phone = models.BooleanField(default=True)
    show_address = models.BooleanField(default=True)
    phone_no = models.CharField(max_length=20, blank=True)
    specialization = models.CharField(max_length=255, default='')
    location = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=255, default='')
    bank = models.CharField(max_length=255, blank=True)
    account_name = models.CharField(max_length=255, default="", blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=50, default='')
    date_of_birth = models.DateField(default=now)

    def user_age(self):
        return now().year - self.date_of_birth.year

    def __str__(self):
        return self.title + ' ' + self.first_name + ' ' + self.last_name

