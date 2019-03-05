from django.db import models


# Create your models here.
class Wallet(models.Model):
    email = models.EmailField()
    acct_name = models.CharField(max_length=255)
    acct_number = models.CharField(max_length=30)
    balance = models.DecimalField(default=0.0, decimal_places=2, max_digits=50)


class Transaction(models.Model):
    sender = models.ForeignKey(Wallet, related_name='sender', on_delete=models.DO_NOTHING)
    receiver = models.ForeignKey(Wallet, related_name='receiver', on_delete=models.DO_NOTHING)
    detail = models.TextField()
    amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=50)
