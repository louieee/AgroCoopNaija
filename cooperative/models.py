from django.db import models
from django.conf import settings
from decimal import Decimal
from django.contrib.auth.models import Group


# Create your models here.
class Cooperative(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    Area_of_Specialization = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image/')
    website = models.URLField()
    email = models.EmailField()
    about = models.TextField()
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    bank = models.CharField(max_length=255)


class Member(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=id)
    date_of_birth = models.DateField()
    time_of_request = models.DateTimeField()
    date_of_admission = models.DateTimeField(blank=True)
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    bank = models.CharField(max_length=255)


class Document(models.Model):
    desc = models.CharField(max_length=255)
    file = models.FileField(upload_to='document/')
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)


class Need(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    amount = models.DecimalField(decimal_places=2, max_digits=50)
    time = models.DateTimeField()
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)


class Loan(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=50)
    granted = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    time_asked = models.DateTimeField()
    time_granted = models.DateTimeField()
    time_to_pay = models.DateTimeField()
    percentage_of_interest = models.DecimalField(default=0.00, decimal_places=2, max_digits=50)
    borrower = models.ForeignKey(Member, on_delete=models.CASCADE)

    def amount_to_pay(self):
        return Decimal(self.amount) + (Decimal(self.amount) * (Decimal(self.percentage_of_interest)/100))


class Collateral(models.Model):
    title = models.CharField(max_length=255)
    document = models.FileField(upload_to='attachment/')
    verified = models.BooleanField(default=False)
    Loan = models.ForeignKey(Loan, on_delete=models.CASCADE)


class Investment(models.Model):
    need = models.ForeignKey(Need, on_delete=models.CASCADE)
    investor = models.ForeignKey(Member, on_delete=models.CASCADE)
    time = models.DateTimeField()
    amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=50)
    payment_proof = models.ImageField(upload_to='image/')
    verified = models.BooleanField(default=False)

    def share(self):
        return (Decimal(self.amount) / Decimal(self.need.amount)) * 100
