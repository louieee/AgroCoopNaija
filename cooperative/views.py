from django.shortcuts import render, redirect, get_object_or_404
import django.utils.timezone as b
from cooperative.models import Cooperative, Member, MembershipRequest, Loan, Investment, Collateral, Need
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


def validate_loan(request, id_, action):
    if request.method == 'POST':
        loan = Loan.objects.get(id=id_)
        loan.status = action
        loan.save()


def validate_investment(request, id_, action):
    if request.method == 'POST':
        investment = Investment.objects.get(id=id_)
        if action == 1:
            investment.verified = True
        elif action == 0:
            investment.verified = False


def react_to_membership_request(request, id_, action):
    if request.method == 'POST':
        request_ = MembershipRequest.objects.get(id=id_)
        if action == 1:
            coop_admin = Member.objects.get(user_id=request.user.id)
            new_member = Member()
            new_member.user_id = request_.sender_id
            new_member.time_of_request = request_.time_of_request
            new_member.cooperative_id = coop_admin.cooperative_id
            new_member.cooperative = coop_admin.cooperative
            new_member.save()
            request_.delete()
        else:
            pass


def all_new_loans(request, id_):
    loans = Cooperative.objects.get(id=id_).all_new_loans
    return render(request, 'cooperative/all_loans.html', {'loans': loans})


def all_new_investments(request, id_):
    investments = Cooperative.objects.get(id=id_).all_new_investments
    return render(request, 'cooperative/all_investments.html', {'investments': investments})


def all_new_needs(request, id_):
    needs = Cooperative.objects.get(id=id_).all_needs
    return render(request, 'cooperative/all_needs.html', {'needs': needs})


def all_new_members(request, id_):
    members = Cooperative.objects.get(id=id_).membership_requests
    return render(request, 'cooperative/all_membership_request.html', {'members': members})


def add_loan(request):
    banks = Bank.bank
    if request.method == 'POST':
        amount = int(request.POST.get('amt', False))
        account_name = str(request.POST.get('acct_name', False))
        account_number = str(request.POST.get('acct_number', False))
        bank = str(request.POST.get('bank', False))
        count = 0
        collateral_list = []
        collateral_names = []
        while request.FILES.get('collateral' + str(count), False):
            collateral_list.append(request.FILES.get('collateral' + str(count), False))
            collateral_names.append(str(request.POST.get('col_title_'+str(count), False)))
        if amount and account_name and account_number and bank:
            if account_name == request.user.account_name and account_number == request.user.account_number and bank == request.user.bank:
                loan = Loan()
                loan.borrower_id = request.user.id
                loan.amount = amount
                loan.time_asked = b.now()
                loan.save()
                for i in range(collateral_list.__len__()):
                    collateral = Collateral()
                    collateral.Loan_id = loan.id
                    collateral.document = collateral_list[i]
                    collateral.title = collateral_names[i]
                    collateral.save()
                return render(request, 'cooperative/add_loan.html',{'message': 'Your Loan request has been sent '
                                                                               'successfully', 'status':'success', 'banks': banks})
            else:
                return render(request, 'cooperative/add_loan.html', {'message': 'Ensure that your account details '
                                                                                'entered tallies with the bank '
                                                                                'details in your profile','status': 'danger', 'banks': banks})
        else:
            return render(request, 'cooperative/add_loan.html', {'message': 'All Fields must be filled', 'status': 'danger', 'banks': banks})
    elif request.method == 'GET':
        return render(request, 'cooperative/add_loan.html', {'banks': banks})


def add_investment(request):
    needs = Need.objects.all()
    if request.method == 'POST':
        amount = int(request.POST.get('amt', False))
        account_number = str(request.POST.get('acct_number', False))
        account_name = str(request.POST.get('acct_name', False))
        need = str(request.POST.get('proof', False))
        if amount and account_number and account_name and need:
            if account_number == request.user.account_number and account_name == request.user.account_name:
                investment = Investment()
                need_ = Need.objects.get(title=need)
                investment.need_id = need_.id
                investment.need = need_
                investment.amount = amount
                investment.investor_id = request.user.id
                investment.time = b.now()
                investment.save()
                return render(request, 'cooperative/add_investment.html', {'message': 'Your Investment has been made '
                                                                                'successfully', 'status': 'success', 'needs':needs})
            else:
                return render(request, 'cooperative/add_investment.html', {'message': 'Ensure that your account details '
                                                                                'entered tallies with the bank '
                                                                                'details in your profile',
                                                                     'status': 'danger', 'needs': needs})
        else:
            return render(request, 'cooperative/add_investment.html',
                          {'message': 'All Fields must be filled', 'status': 'danger', 'needs': needs})
    elif request.method == 'GET':
        return render(request, 'cooperative/add_investment.html')


def add_need(request):
    return render(request, 'cooperative/add_need.html')
