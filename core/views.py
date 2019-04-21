import re
from django.shortcuts import render, redirect
from Lists import Bank, Tag
from core.models import User
from django.utils.timezone import datetime
from django.contrib import auth
from cooperative.models import Member
from partner.models import Partner


def sign_up(request):
    banks = Bank.bank
    tags = Tag.tags
    if request.method == 'POST':
        fn = str(request.POST.get('fn', False))
        ln = str(request.POST.get('ln', False))
        username = str(request.POST.get('username', False))
        dob = str(request.POST.get('dob', False))
        spec = str(request.POST.get('spec', False))
        gender = str(request.POST.get('gender', False))
        email = str(request.POST.get('email', False))
        phone = str(request.POST.get('phone', False))
        bank = str(request.POST.get('bank', False))
        account_num = str(request.POST.get('acct_num', False))
        pass1 = str(request.POST.get('pass1', False))
        pass2 = str(request.POST.get('pass2', False))
        if fn and ln and phone and email and dob and account_num and spec and gender and username and pass1 and pass2:
            if pass1 == pass2:
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    try:
                        user_ = User.objects.get(username=username)
                    except User.DoesNotExist:
                        my_user = User.objects.create_user(username, email, pass1)
                        my_user.first_name = fn
                        my_user.last_name = ln
                        dob1 = re.split('-', dob)
                        my_user.date_of_birth = datetime(year=int(dob1[0]), month=int(dob1[1]), day=int(dob1[2]))
                        my_user.phone_no = phone
                        my_user.gender = gender
                        my_user.specialization = spec
                        my_user.bank = bank
                        my_user.account_number = account_num
                        my_user.save()
                        return render(request, 'core/home.html',
                                      {'message': 'Your Account Has Been Created Successfully', 'status': 'success'})
                    else:
                        return render(request, 'core/login.html',
                                      {'message': 'This Username is in use by another user',
                                       'status': 'danger', 'banks': banks, 'tags': tags})
                else:
                    return render(request, 'core/login.html',
                                  {'message': 'This Email address is in use by another user',
                                   'status': 'danger', 'banks': banks, 'tags': tags})
            else:
                return render(request, 'core/login.html', {'message': 'The two passwords does not match',
                                                           'status': 'danger', 'banks': banks, 'tags': tags})
        else:
            return render(request, 'core/login.html', {'message': 'All fields must be filled',
                                                       'status': 'danger', 'banks': banks, 'tags': tags})

    return render(request, 'core/login.html', {'banks': banks, 'tags': tags})


def dashboard(request):
    return render(request, 'core/Dashboard.html')


def login(request):
    if request.method == 'POST':
        username = str(request.POST.get('username2', False))
        password = str(request.POST.get('password', False))
        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('home')
            else:
                message = 'Username or Password is Incorrect'
                return render(request, 'core/login.html',
                              {'message': message, 'status': 'danger', 'user': username, 'pass': password})

        else:
            message = 'All Fields must be filled'
            return render(request, 'core/login.html',
                          {'message': message, 'status': 'danger', 'user': username, 'pass': password})

    return render(request, 'core/login.html')


def profile(request, id_):
    user = User.objects.get(id=id_)
    member = Member.objects.get(id=user.id)
    partner = Partner.objects.get(id=user.id)
    return render(request, 'core/profile.html', {'user': user, 'member': member, 'partner':partner})
