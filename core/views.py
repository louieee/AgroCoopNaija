from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import auth
from django.conf import settings
from core.models import User
from product.models import Order
from wallet.models import Wallet, Transaction
from django.contrib.auth.hashers import MD5PasswordHasher as Hash


def sign_up(request):
    if request.method == 'POST':
        fn = request.POST.get('fn', False)
        ln = request.POST.get('ln', False)
        phone = request.POST.get('phone', False)
        email = request.POST.get('email', False)
        username = request.POST.get('username', False)
        image = request.FILES.get('image', False)
        pass1 = request.POST.get('pass1', False)
        pass2 = request.POST.get('pass2', False)
        if fn and ln and phone and email and username and pass1 and pass2:
            if pass1 == pass2:
                user = User.objects.get(email=email)
                if user.DoesNotExist:
                    user_ = User.objects.get(username=username)
                    if user_.DoesNotExist:
                        my_user = User()
                        my_user.first_name = fn
                        my_user.last_name = ln
                        my_user.phone_no = phone
                        my_user.image = image
                        my_user.username = username
                        my_user.email = email
                        my_user.password = pass1
                        my_user.save()
                        user_wallet = Wallet()
                        user_wallet.email = email
                        user_wallet.acct_name = username
                        user_wallet.acct_number = Hash().salt()
                        user_wallet.save()
                        return redirect('home',
                                        {'message': 'Your account has been created successfully', 'status': 'success'})
                    else:
                        return render(request, 'core/signup.html',
                                      {'message': 'This Username is in use by another user',
                                       'status': 'danger'})
                else:
                    return render(request, 'core/signup.html',
                                  {'message': 'This Email address is in use by another user',
                                   'status': 'danger'})
            else:
                return render(request, 'core/signup.html', {'message': 'The two passwords does not match',
                                                            'status': 'danger'})
        else:
            return render(request, 'core/signup.html', {'message': 'All fields must be filled',
                                                        'status': 'danger'})

    return render(request, 'core/signup.html')


def dashboard(request, username):
    customer = get_object_or_404(settings.AUTH_USER_MODEL, username=username)
    user = auth.get_user_model()
    m_wallet = get_object_or_404(Wallet, user=user)
    transactions = get_list_or_404(Transaction, sender=m_wallet)
    orders = get_list_or_404(Order, customer=user)
    return render(request, 'core/dashboard.html', {'customer': customer, 'wallet': m_wallet,
                                                   'transactions': transactions, 'orders': orders})


def login(request):
    return render(request, 'core/login.html')
