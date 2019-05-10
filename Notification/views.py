from .models import ViewedNeedNotification, ViewedMembershipNotification, ViewedInvestmentNotification, \
    ViewedLoanNotification
from django.shortcuts import HttpResponse


# Create your views here.
def add_to_need_list(request):
    if request.method == 'GET':
        id1 = int(request.GET['id'])
        id2 = int(request.GET['id_not'])
        try:
            ViewedNeedNotification.objects.get(notification_id=id2, need_id=id1)
            return HttpResponse('success')
        except ViewedNeedNotification.DoesNotExist:
            my_list = ViewedNeedNotification()
            my_list.need_id = id1
            my_list.notification_id = id2
            my_list.save()
            return HttpResponse('success')


def add_to_loan_list(request):
    if request.method == 'GET':
        id1 = int(request.GET['id'])
        id2 = int(request.GET['id_not'])
        try:
            ViewedLoanNotification.objects.get(notification_id=id2, loan_id=id1)
            return HttpResponse('success')
        except ViewedLoanNotification.DoesNotExist:
            my_list = ViewedLoanNotification()
            my_list.loan_id = id1
            my_list.notification_id = id2
            my_list.save()
            return HttpResponse('success')


def add_to_invest_list(request):
    if request.method == 'GET':
        id1 = int(request.GET['id'])
        id2 = int(request.GET['id_not'])
        try:
            ViewedInvestmentNotification.objects.get(notification_id=id2, investment_id=id1)
            return HttpResponse('success')
        except ViewedInvestmentNotification.DoesNotExist:
            my_list = ViewedInvestmentNotification()
            my_list.investment_id = id1
            my_list.notification_id = id2
            my_list.save()
            return HttpResponse('success')


def add_to_member_list(request):
    if request.method == 'GET':
        id1 = int(request.GET['id'])
        id2 = int(request.GET['id_not'])
        try:
            ViewedMembershipNotification.objects.get(notification_id=id2, membership_id=id1)
            return HttpResponse('success')
        except ViewedMembershipNotification.DoesNotExist:
            my_list = ViewedMembershipNotification()
            my_list.membership_id = id1
            my_list.notification_id = id2
            my_list.save()
            return HttpResponse('success')
