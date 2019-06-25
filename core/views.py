import re
from django.shortcuts import render, redirect
from my_methods import Bank, Tag, State
from core.models import User
from django.utils.timezone import datetime
from django.contrib import auth
from cooperative.models import Member, Cooperative
from partner.models import Partner


# This view takes values values from the signup form and adds a new user to the database
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
                                                           'status': 'danger', 'banks': banks, 'tags': tags,
                                                           'states': states})
        else:
            return render(request, 'core/login.html', {'message': 'All fields must be filled',
                                                       'status': 'danger', 'banks': banks, 'tags': tags,
                                                       'states': states})
    else:
        return render(request, 'core/login.html', {'banks': banks, 'tags': tags, 'states': states})


# This view collects all the user's information from the database and displays it onto
# the dashboard page
def dashboard(request):
    banks = Bank.bank
    tags = Tag.tags
    user = User.objects.get(id=request.user.id)
    if request.user.is_partner and request.user.is_cooperative_member:
        partner = Partner.objects.get(user_id=user.id)
        coop_mem = Member.objects.get(user_id=user.id)
        coop = Cooperative.objects.get(id=coop_mem.cooperative_id)
        return render(request, 'core/Dashboard.html', {'partner': partner, 'member': coop_mem, 'coop': coop,
                                                       'banks': banks, 'tags': tags})
    else:
        if request.user.is_partner:
            partner = Partner.objects.get(user_id=user.id)
            return render(request, 'core/Dashboard.html', {'partner': partner})
        elif request.user.is_cooperative_member:
            coop_mem = Member.objects.get(user_id=user.id)
            coop = Cooperative.objects.get(id=coop_mem.cooperative_id)
            return render(request, 'core/Dashboard.html', {'member': coop_mem, 'coop': coop,
                                                           'banks': banks, 'tags': tags
                                                           })
        else:
            return render(request, 'core/Dashboard.html', {
                                                           'banks': banks, 'tags': tags
                                                           })



# This view takes in user's username and password and logs the user in
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


# This view takes user's information from database and displays it onto the user's profile page
def profile(request, id_):
    user = User.objects.get(id=id_)
    try:
        member = Member.objects.get(user_id=user.id)
        try:
            partner = Partner.objects.get(user_id=user.id)
            if user.is_partner and user.is_cooperative_member:
                return render(request, 'core/profile.html', {'user': user, 'member': member, 'partner': partner})
            else:
                if user.is_cooperative_member:
                    return render(request, 'core/profile.html', {'user': user, 'member': member})
                elif user.is_partner:
                    return render(request, 'core/profile.html', {'user': user, 'partner': partner})
                else:
                    return render(request, 'core/profile.html', {'user': user})
        except Partner.DoesNotExist:
            if user.is_cooperative_member:
                return render(request, 'core/profile.html', {'user': user, 'member': member})
            else:
                return render(request, 'core/profile.html', {'user': user})
    except Member.DoesNotExist:
        try:
            partner = Partner.objects.get(user_id=user.id)
            return render(request, 'core/profile.html', {'user': user, 'partner': partner})
        except Partner.DoesNotExist:
            return render(request, 'core/profile.html', {'user': user})


# This view enables a user to update his/her profile information in the database
def update_profile(request):
    if request.method == 'POST':
        email = request.POST.get('email', False)
        image = request.FILES.get('profile_pic', False)
        phone = request.POST.get('phone', False)
        bank = request.POST.get('bank', False)
        icon = request.FILES.get("icon", False)
        account_name = request.POST.get('acct_name', False)
        account_num = request.POST.get('acct_num', False)
        bio = request.POST.get('bio', False)
        if phone and email:
            my_user = User.objects.get(username=request.user.username)
            if str(request.user.email) == str(email):
                my_user.email = str(email)
            else:
                try:
                    user = User.objects.get(email=str(email))
                except User.DoesNotExist:
                    my_user.email = str(email)
            my_user.phone_no = str(phone)
            if bank:
                my_user.bank = str(bank)
            if account_num:
                my_user.account_number = str(account_num)
            if account_name:
                my_user.account_name = str(account_name)
            if image:
                my_user.image = image
            my_user.save()

        if request.user.is_partner:
            partner = Partner.objects.get(user_id=request.user.id)
            if bio:
                partner.biography = str(bio)
            if icon:
                partner.icon = icon
            partner.save()
        return redirect('/account/dashboard')
