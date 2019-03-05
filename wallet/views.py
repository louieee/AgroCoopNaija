from django.shortcuts import render, get_object_or_404
from wallet.models import Wallet
from django.conf import settings


# Create your views here.
def wallet(request, email):
    wallet_ = get_object_or_404(Wallet, user=get_object_or_404(settings.AUTH_USER_MODEL, email=email))
    return render(request, '../wallet/templates/wallet/wallet.html', {'wallet': wallet_})
