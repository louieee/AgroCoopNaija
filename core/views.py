from django.shortcuts import render, redirect
from core.models import User, Bank


def sign_up(request):
    banks = Bank.bank
    if request.method == 'POST':
        fn = request.POST.get('fn', False)
        ln = request.POST.get('ln', False)
        phone = request.POST.get('phone', False)
        email = request.POST.get('email', False)
        is_partner = request.POST.get('coop', False)
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
                        my_user = User.objects.create_user(username, email, pass1)
                        my_user.first_name = fn
                        my_user.last_name = ln
                        my_user.phone_no = phone
                        my_user.image = image
                        my_user.save()
                        if is_partner == "True":
                            return redirect('be_partner')
                        elif is_partner == "False":
                            return redirect('be_member')
                    else:
                        return render(request, 'core/signup.html',
                                      {'message': 'This Username is in use by another user',
                                       'status': 'danger', 'banks': banks})
                else:
                    return render(request, 'core/signup.html',
                                  {'message': 'This Email address is in use by another user',
                                   'status': 'danger', 'banks': banks})
            else:
                return render(request, 'core/signup.html', {'message': 'The two passwords does not match',
                                                            'status': 'danger', 'banks': banks})
        else:
            return render(request, 'core/signup.html', {'message': 'All fields must be filled',
                                                        'status': 'danger', 'banks': banks})

    return render(request, 'core/signup.html', {'banks': banks})




def login(request):
    return render(request, 'core/login.html')
