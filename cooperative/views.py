from django.shortcuts import render, redirect, get_object_or_404
import django.utils.timezone as b
from cooperative.models import Cooperative, Member, MembershipRequest
from Lists import Tag, Bank, State


# Create your views here.
def create_coop(request):
    tags = Tag.tags
    banks = Bank.bank
    states = State.states
    if request.method == 'POST':
        name = str(request.POST.get('name', False))
        reg_no = str(request.POST.get('reg_no', False))
        location = str(request.POST.get('location', False))
        website = str(request.POST.get('website', False))
        phone = str(request.POST.get('phone', False))
        email = str(request.POST.get('email', False))
        bank = str(request.POST.get('bank', False))
        specialization = str(request.POST.get('area_of_spec', False))
        account_name = str(request.POST.get('acct_name', False))
        account_number = str(request.POST.get('acct_num', False))
        desc = str(request.POST.get('desc', False))
        if name and location and phone and website and email and desc and bank and account_name and account_number and reg_no:
            try:
                Cooperative.objects.get(reg_no=reg_no)
            except Cooperative.DoesNotExist:
                try:
                    Cooperative.objects.get(name=name)
                except Cooperative.DoesNotExist:
                    coop = Cooperative()
                    coop.name = name
                    coop.location = location
                    coop.Area_of_Specialization = specialization
                    coop.account_name = account_name
                    coop.account_number = account_number
                    coop.reg_no = reg_no
                    coop.phone = phone
                    coop.website = website
                    coop.about = desc
                    coop.email = email
                    coop.save()
                    return redirect('home', {'message': 'Your Cooperative has been created', 'status': 'success'})
                else:
                    return render(request, 'cooperative/create_coop.html',
                                  {'message': 'A cooperative already has this email address',
                                   'status': 'danger', 'tags': tags, 'banks': banks, 'states': states})
            else:
                return render(request, 'cooperative/create_coop.html',
                              {'message': 'A cooperative with this name already exists',
                               'status': 'danger', 'tags': tags, 'banks': banks, 'states': states})
        else:
            return render(request, 'cooperative/create_coop.html',
                          {'message': 'All fields must be filled',
                           'status': 'danger', 'tags': tags, 'banks': banks, 'states': states})
    return render(request, 'cooperative/create_coop.html', {'tags': tags, 'banks': banks, 'states': states})


def be_coop_member(request, id_):
    if request.method == 'POST':
        coop = Cooperative.objects.get(id=id_)
        if request.user.is_authenticated:
            try:
                MembershipRequest.objects.get(sender_id=request.user.id,
                                              cooperative=coop, email=request.user.email)
            except MembershipRequest.DoesNotExist:
                request_ = MembershipRequest()
                request_.sender_id = request.user.id
                request_.time_of_request = b.now()
                request_.name = request.user.first_name + " " + request.user.last_name
                request_.cooperative = coop
                request_.email = request.user.email
                request_.save()
                return render(request, 'cooperative/coop_detail.html',
                              {'message': 'You have Successfully sent a Membership Request to ' + coop.name,
                               'status': 'success', 'coop': coop})
            else:
                return render(request, 'cooperative/coop_detail.html',
                                {'message': 'You have previously sent a Membership Request to ' + coop.name,
                                 'status': 'info', 'coop': coop})

        else:
            return render(request, 'cooperative/coop_detail.html',
                            {'message': 'You must be logged in to send a request ' + coop.name,
                             'status': 'danger', 'coop': coop})


def all_cooperatives(request):
    all_coop = Cooperative.objects.all()
    return render(request, 'cooperative/all_cooperatives.html', {'cooperatives': all_coop})


def invest(request):
    return render(request, 'cooperative/invest_form.html')


def request_loan(request):
    return render(request, 'cooperative/loan_form.html')


def coop_detail(request, _id):
    coop = get_object_or_404(Cooperative, id=_id)
    rel_coop = Cooperative.objects.all().filter(Area_of_Specialization=coop.Area_of_Specialization)
    return render(request, 'cooperative/coop_detail.html', {'coop': coop, 'rel': rel_coop})
