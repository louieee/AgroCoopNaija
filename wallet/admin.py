from django.contrib import admin
from wallet.models import Transaction, Wallet
# Register your models here.
admin.site.register(Transaction)
admin.site.register(Wallet)

