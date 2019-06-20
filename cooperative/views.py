from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
import django.utils.timezone as b
from cooperative.models import Cooperative, Member, MembershipRequest, Loan, Investment, Collateral, Need
from my_methods import Tag, Bank, State, get_pagination
from datetime import datetime as d
from Notification.models import Notification, ViewedNeedNotification
from core.models import User
import re


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
        motto = str(request.POST.get('motto', False))
        account_name = str(request.POST.get('acct_name', False))
        account_number = str(request.POST.get('acct_number', False))
        desc = str(request.POST.get('desc', False))
        if name and phone and website and email and desc and account_name and account_number and reg_no and motto:
            try:
                Cooperative.objects.get(reg_no=reg_no)
            except Cooperative.DoesNotExist:
                try:
                    Cooperative.objects.get(name=name)
                except Cooperative.DoesNotExist:
                    coop = Cooperative()
                    coop.name = name
                    coop.motto = motto
                    coop.location = location
                    coop.bank = bank
                    coop.Area_of_Specialization = specialization
                    coop.account_name = account_name
                    coop.account_number = account_number
                    coop.reg_no = reg_no

                    coop.phone = phone
                    coop.website = website
                    coop.about = desc
                    coop.email = email
                    coop.save()
                    return render(request, 'core/home.html',
                                  {'message': 'Your Cooperative has been created', 'status': 'success'})
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


def all_cooperatives(request, page):
    all_coop = Cooperative.objects.all().order_by('id')
    pages = get_pagination(page, all_coop)
    return render(request, 'cooperative/all_cooperatives.html', {'cooperatives': all_coop, 'pages': pages})


def coop_detail(request, _id):
    coop = get_object_or_404(Cooperative, id=_id)
    rel_coop = Cooperative.objects.all().filter(Area_of_Specialization=coop.Area_of_Specialization)
    return render(request, 'cooperative/coop_detail.html', {'coop': coop, 'rel': rel_coop})


def validate_loan(request, id_):
    if request.method == 'POST':
        loan = Loan.objects.get(id=id_)
        if 'Grant' in request.POST:
            action = 'G'
            d_o_p = str(request.POST.get('date_of_payment', False))
            loan.status = action
            loan.time_granted = d.now()
            dob1 = re.split('-', d_o_p)
            loan.time_to_pay = d(year=int(dob1[0]), month=int(dob1[1]), day=int(dob1[2]))
            loan.save()
            return redirect('/account/dashboard/')
            # return render (request, 'core/Dashboard.html', {'message':'Loan has been Granted', 'status':'success'})
        elif 'Decline' in request.POST:
            action = 'D'
            loan.status = action
            loan.save()
            return redirect('/account/dashboard/')
            # return render(request, 'core/Dashboard.html', {'message': 'Loan has been Declined', 'status': 'success'})


def validate_investment(request, id_, action):
    if request.method == 'GET':
        investment = Investment.objects.get(id=id_)
        if action == 1:
            investment.verified = True
            investment.save()
            return redirect('/account/dashboard/')
        elif action == 0:
            investment.verified = False
            investment.save()
            return redirect('/account/dashboard/')


def react_to_membership_request(request, id_, action):
    if request.method == 'GET':
        request_ = MembershipRequest.objects.get(id=id_)
        if action == 1:
            coop_admin = Member.objects.get(user_id=request.user.id)
            new_member = Member()
            new_member.user_id = request_.sender_id
            new_member.time_of_request = request_.time_of_request
            new_member.date_of_admission = d.now()
            new_member.cooperative_id = coop_admin.cooperative_id
            new_member.cooperative = coop_admin.cooperative
            new_member.save()
            my_user = User.objects.get(id=new_member.user_id)
            my_user.is_cooperative_member = True
            my_user.save()
            notification = Notification()
            notification.member = new_member
            notification.save()
            request_.delete()
            return redirect('/account/dashboard/')
            # {'message': str(my_user.first_name) + " " + str(my_user.last_name) + " is now a member of "
            #             + str(Cooperative.objects.get(id=coop_admin.cooperative_id).name),
            #  'status': 'success'})
        elif action == 0:
            request_.delete()
            return redirect('/account/dashboard/')
            # return render(request, 'core/Dashboard.html',
            #               {'message': 'The request has been declined and deleted', 'status': 'success'})


def all_new_loans(request, id_):
    coop = Cooperative.objects.get(id=id_)
    return render(request, 'cooperative/all_loans.html', {'coop': coop})


def all_new_investments(request, id_):
    coop = Cooperative.objects.get(id=id_)
    return render(request, 'cooperative/all_investments.html', {'coop': coop})


def all_new_needs(request, id_, page):
    coop = Cooperative.objects.get(id=id_)
    needs = coop.all_needs()
    pages = get_pagination(page, needs)
    return render(request, 'cooperative/all_needs.html', {'needs': pages, 'coop': coop})


def all_new_members(request, id_, page):
    coop = Cooperative.objects.get(id=id_)
    pages = get_pagination(page, coop.membership_requests())
    return render(request, 'cooperative/all_membership_request.html', {'members': pages, 'coop': coop})


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
        while request.FILES.get('collateral' + str(count), False) is not False:
            collateral_list.append(request.FILES.get('collateral' + str(count), False))
            collateral_names.append(str(request.POST.get('col_title_' + str(count), False)))
            count = count + 1
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
                return render(request, 'cooperative/add_loan.html', {'message': 'Your Loan request has been sent '
                                                                                'successfully', 'status': 'success',
                                                                     'banks': banks})
            else:
                return render(request, 'cooperative/add_loan.html', {'message': 'Ensure that your account details '
                                                                                'entered tallies with the bank '
                                                                                'details in your profile',
                                                                     'status': 'danger', 'banks': banks})
        else:
            return render(request, 'cooperative/add_loan.html',
                          {'message': 'All Fields must be filled', 'status': 'danger', 'banks': banks})
    elif request.method == 'GET':
        return render(request, 'cooperative/add_loan.html', {'banks': banks})


def add_investment(request, id_):
    need_ = Need.objects.get(id=id_)
    if request.method == 'POST':
        amount = int(request.POST.get('amt', False))
        account_number = str(request.POST.get('acct_number', False))
        account_name = str(request.POST.get('acct_name', False))
        proof = request.FILES.get('proof', False)
        if amount and account_number and account_name and proof:
            if account_number == request.user.account_number and account_name == request.user.account_name:
                member = Member.objects.get(user_id=request.user.id)
                coop = Cooperative.objects.get(id=member.cooperative_id)
                investment = Investment()
                investment.need_id = need_.id
                investment.need = need_
                investment.payment_proof = proof
                investment.amount = amount
                investment.cooperative = coop
                investment.cooperative_id = coop.id
                investment.investor_id = request.user.id
                investment.time = b.now()
                no = Notification.objects.get(member_id=request.user.id)
                nn = ViewedNeedNotification()
                nn.notification_id = no.id
                nn.need_id = need_.id
                nn.save()
                investment.save()
                return render(request, 'cooperative/add_investment.html', {'message': 'Your Investment has been made '
                                                                                      'successfully',
                                                                           'status': 'success', 'need': need_})
            else:
                return render(request, 'cooperative/add_investment.html',
                              {'message': 'Ensure that your account details '
                                          'entered tallies with the bank '
                                          'details in your profile',
                               'status': 'danger', 'need': need_})
        else:
            return render(request, 'cooperative/add_investment.html',
                          {'message': 'All Fields must be filled', 'status': 'danger', 'need': need_})
    elif request.method == 'GET':
        return render(request, 'cooperative/add_investment.html', {'need': need_})


def add_need(request):
    if request.method == 'POST':
        title = str(request.POST.get('need_title', False))
        body = str(request.POST.get('need_body', False))
        time = str(request.POST.get('need_time', False))
        amount = str(request.POST.get('amt', False))
        count = 0
        document_list = []
        while request.FILES.get('document' + str(count), False) is not False:
            document_list.append(request.FILES.get('document' + str(count), False))
            count = count + 1
        if title and body and time and amount:
            member = Member.objects.get(user_id=request.user.id)
            coop = Cooperative.objects.get(id=member.cooperative_id)
            need = Need()
            to = re.split('-', time)
            too = re.split('T', to[2])
            tooo = re.split(':', too[1])
            need.time = d(year=int(to[0]), month=int(to[1]), day=int(too[0]), hour=int(tooo[0]), minute=int(tooo[1]))
            need.amount = amount
            need.cooperative = coop
            need.cooperative_id = coop.id
            need.body = body
            need.title = title
            need.save()
            return render(request, 'cooperative/add_need.html', {'message': 'The Need has been Created '
                                                                            'successfully', 'status': 'success'})
        else:
            return render(request, 'cooperative/add_need.html',
                          {'message': 'All Fields Must Be Filled', 'status': 'danger'})
    elif request.method == 'GET':
        return render(request, 'cooperative/add_need.html')


def investment_detail(request, coop_name, id_):
    coop = Cooperative.objects.get(name=coop_name)
    investment = Investment.objects.get(id=id_)
    return render(request, 'cooperative/investment_detail.html', {'invest': investment, 'coop': coop})


def membership_request_detail(request, coop_name, id_):
    coop = Cooperative.objects.get(name=coop_name)
    membership_request = MembershipRequest.objects.get(id=id_)
    return render(request, 'cooperative/membership_request_detail.html',
                  {'membership_request': membership_request, 'coop': coop})


def loan_detail(request, coop_name, id_):
    coop = Cooperative.objects.get(name=coop_name)
    loan = Loan.objects.get(id=id_)
    return render(request, 'cooperative/loan_detail.html', {'loan': loan, 'coop': coop})


def need_detail(request, coop_name, id_):
    coop = Cooperative.objects.get(name=coop_name)
    investment = Investment.objects.get(investor_id=request.user.id, need_id=id_, cooperative_id=coop.id)
    need = Need.objects.get(id=id_)
    return render(request, 'cooperative/need_detail.html', {'need': need, 'coop': coop, 'investment': investment})


def all_members(request, coop_name, page):
    coop = Cooperative.objects.get(name=coop_name)
    pages = get_pagination(page, coop.all_members())
    return render(request, 'cooperative/all_members.html', {'coop': coop, 'members_list': pages})


def all_investors(request, need_title, page):
    need = Need.objects.get(title=need_title)
    investments = need.all_investments()
    pages = get_pagination(page, investments)
    return render(request, 'cooperative/all_investors.html', {'investments': pages, 'need': need})


def all_coop_post(request, id_, page):
    coop = Cooperative.objects.get(id=id_)
    coop_posts = get_pagination(page,coop.all_posts())
    return render(request, 'cooperative/all_cooperative_post.html', {'coop': coop, 'coop_posts': coop_posts})
