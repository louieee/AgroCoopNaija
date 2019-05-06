from django.shortcuts import render
from .models import ViewedNeedNotification, ViewedMembershipNotification, ViewedInvestmentNotification, \
    ViewedLoanNotification


# Create your views here.
def add_to_need_list(request, id_):
    if request.method == 'POST':
        try:
            ViewedNeedNotification.objects.get(member__user_id=request.user.id, need_id=id_)
        except ViewedNeedNotification.DoesNotExist:
            my_need_list = ViewedNeedNotification()
            my_need_list.member_id = request.user.id
            my_need_list.need_id = id_
            my_need_list.save()


def add_to_loan_list(request, id_):
    if request.method == 'POST':
        try:
            ViewedLoanNotification.objects.get(member__user_id=request.user.id, loan_id=id_)
        except ViewedLoanNotification.DoesNotExist:
            my_list = ViewedLoanNotification()
            my_list.member_id = request.user.id
            my_list.loan_id = id_
            my_list.save()


def add_to_invest_list(request, id_):
    if request.method == 'POST':
        try:
            ViewedInvestmentNotification.objects.get(member__user_id=request.user.id, investment_id=id_)
        except ViewedInvestmentNotification.DoesNotExist:
            my_list = ViewedInvestmentNotification()
            my_list.member_id = request.user.id
            my_list.investment_id = id_
            my_list.save()


def add_to_member_list(request, id_):
    if request.method == 'POST':
        try:
            ViewedMembershipNotification.objects.get(member__user_id=request.user.id, membership_id=id_)
        except ViewedMembershipNotification.DoesNotExist:
            my_list = ViewedMembershipNotification()
            my_list.member_id = request.user.id
            my_list.membership_id = id_
            my_list.save()
