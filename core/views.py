import re
from django.shortcuts import render, redirect
from Lists import Bank, Tag, State
from core.models import User
from django.utils.timezone import datetime
from django.contrib import auth
from cooperative.models import Member, Cooperative
from partner.models import Partner
from Notification.models import Notification


def sign_up(request):
    banks = Bank.bank
    tags = Tag.tags
    states = State.states
    if request.method == 'POST':
        fn = str(request.POST.get('fn', False))
        ln = str(request.POST.get('ln', False))
        username = str(request.POST.get('username', False))
        dob = str(request.POST.get('dob', False))
        spec = str(request.POST.get('spec', False))
        gender = str(request.POST.get('gender', False))
        location = str(request.POST.get('location', False))
        email = str(request.POST.get('email', False))
        phone = str(request.POST.get('phone', False))
        bank = str(request.POST.get('bank', False))
        account_name = str(request.POST.get('acct_name', False))
        account_num = str(request.POST.get('acct_num', False))
        pass1 = str(request.POST.get('pass1', False))
        pass2 = str(request.POST.get('pass2', False))
        if fn and ln and phone and email and dob and location and account_num and account_name and spec and gender and username and pass1 and pass2:
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
                        my_user.location = location
                        my_user.account_number = account_num
                        my_user.account_name = account_name
                        my_user.save()
                        return render(request, 'core/home.html',
                                      {'message': 'Your Account Has Been Created Successfully', 'status': 'success'})
                    else:
                        return render(request, 'core/login.html',
                                      {'message': 'This Username is in use by another user',
                                       'status': 'danger', 'banks': banks, 'tags': tags, 'states': states})
                else:
                    return render(request, 'core/login.html',
                                  {'message': 'This Email address is in use by another user',
                                   'status': 'danger', 'banks': banks, 'tags': tags, 'states': states})
            else:
                return render(request, 'core/login.html', {'message': 'The two passwords does not match',
                                                           'status': 'danger', 'banks': banks, 'tags': tags, 'states': states})
        else:
            return render(request, 'core/login.html', {'message': 'All fields must be filled',
                                                       'status': 'danger', 'banks': banks, 'tags': tags, 'states': states})
    else:
        return render(request, 'core/login.html', {'banks': banks, 'tags': tags, 'states': states})


def dashboard(request):
    banks = Bank.bank
    tags = Tag.tags
    user = User.objects.get(id=request.user.id)
    if request.user.is_partner and request.user.is_cooperative_member:
        partner = Partner.objects.get(user_id=user.id)
        coop_mem = Member.objects.get(user_id=user.id)
        notifications = Notification.objects.get(member__user_id=request.user.id)
        coop = Cooperative.objects.get(id=coop_mem.cooperative_id)
        return render(request, 'core/Dashboard.html', {'partner': partner, 'member': coop_mem, 'coop': coop,
                                                       'banks': banks, 'tags': tags, 'notifications': notifications})
    else:
        if request.user.is_partner:
            partner = Partner.objects.get(user_id=user.id)
            return render(request, 'core/Dashboard.html', {'partner': partner})
        elif request.user.is_partner:
            coop_mem = Member.objects.get(user_id=user.id)
            coop = Cooperative.objects.get(id=coop_mem.cooperative_id)
            notifications = Notification.objects.get(member__user_id=request.user.id)
            if notifications.DoesNotExist:
                return render(request, 'core/Dashboard.html', {'member': coop_mem, 'coop': coop,
                                                               'banks': banks, 'tags': tags
                                                               })
            else:
                return render(request, 'core/Dashboard.html', {'member': coop_mem, 'coop': coop,
                                                               'banks': banks, 'tags': tags, 'notifications': notifications})
        else:
            return render(request, 'core/Dashboard.html')


def login(request):
    banks = Bank.bank
    tags = Tag.tags
    states = State.states
    if request.method == 'POST':
        username = str(request.POST.get('username2', False))
        password = str(request.POST.get('password', False))
        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            else:
                message = 'Username or Password is Incorrect'
                return render(request, 'core/login.html',
                              {'message': message, 'status': 'danger', 'user': username, 'pass': password})

        else:
            message = 'All Fields must be filled'
            return render(request, 'core/login.html',
                          {'message': message, 'status': 'danger', 'user': username, 'pass': password})

    return render(request, 'core/login.html', {'banks': banks, 'tags': tags, 'states': states})


def profile(request, id_):
    pat = False
    mem = False
    user = User.objects.get(id=id_)
    try:
        Member.objects.get(user_id=user.id)
    except Member.DoesNotExist:
        try:
            Partner.objects.get(user_id=user.id)
        except Partner.DoesNotExist:
            return render(request, 'core/profile.html', {'user': user})
        else:
            pat = True
    else:
        mem = True
    if mem is True and pat is True:
        member = Member.objects.get(user_id=user.id)
        partner = Partner.objects.get(user_id=user.id)
        return render(request, 'core/profile.html', {'user': user, 'member': member, 'partner': partner})
    else:
        if mem is True:
            member = Member.objects.get(user_id=user.id)
            return render(request, 'core/profile.html', {'user': user, 'member': member})
        elif pat is True:
            partner = Partner.objects.get(user_id=user.id)
            return render(request, 'core/profile.html', {'user': user, 'partner': partner})


def update_profile(request):
    if request.method == 'POST':
        email = str(request.POST.get('email', False))
        image = request.FILES.get('profile_pic', False)
        phone = str(request.POST.get('phone', False))
        bank = str(request.POST.get('bank', False))
        icon = request.FILES.get("icon", False)
        account_name = str(request.POST.get('acct_name', False))
        account_num = str(request.POST.get('acct_num', False))
        bio = request.POST.get('bio', False)
        if phone and email:
            my_user = User.objects.get(username=request.user.username)
            if str(request.user.email) == email:
                my_user.email = email
            else:
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    my_user.email = email
            my_user.phone_no = phone
            if (bank is not False) or bank != 'False':
                my_user.bank = bank
            if (account_num is not False) or account_num != 'False':
                my_user.account_number = account_num
            if (account_name is not False) or account_name != 'False':
                my_user.account_name = account_name
            if (image is not False) or bank != 'False':
                my_user.image.file = image
            my_user.save()

        if request.user.is_partner:
            partner = Partner.objects.get(user_id=request.user.id)
            if (bio is not False) or bio != 'False':
                partner.biography = bio
            if icon is not False:
                partner.icon = icon
            partner.save()
        return redirect('/account/dashboard')
