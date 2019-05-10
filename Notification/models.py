from django.db import models
from cooperative.models import Member, Cooperative, Loan, Investment, MembershipRequest, Need


# Create your models here.
class Notification(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)

    def loan_display(self):
        coop_id = Member.objects.get(user_id=self.member_id).cooperative_id
        all_new_loan = len(Cooperative.objects.get(id=coop_id).all_new_loans())
        viewed_loan = len(ViewedLoanNotification.objects.filter(notification_id=self.id).all())
        return int(all_new_loan) - int(viewed_loan)

    def need_display(self):
        coop_id = Member.objects.get(user_id=self.member_id).cooperative_id
        all_new_need = len(Cooperative.objects.get(id=coop_id).all_needs())
        viewed_need = len(ViewedNeedNotification.objects.filter(notification_id=self.id).all())
        return int(all_new_need) - int(viewed_need)

    def membership_display(self):
        coop_id = Member.objects.get(user_id=self.member_id).cooperative_id
        new_membership = len(Cooperative.objects.get(id=coop_id).membership_requests())
        viewed_membership = len(ViewedMembershipNotification.objects.filter(notification_id=self.id).all())
        return int(new_membership) - int(viewed_membership)

    def investment_display(self):
        coop_id = Member.objects.get(user_id=self.member_id).cooperative_id
        new_investment = len(Cooperative.objects.get(id=coop_id).all_new_investments())
        viewed_investment = len(ViewedInvestmentNotification.objects.filter(notification_id=self.id).all())
        return int(new_investment) - int(viewed_investment)

    def loan_viewed_list(self):
        my_loan_list = []
        for loan in ViewedLoanNotification.objects.filter(notification_id=self.id).all():
            my_loan_list.append(loan.loan_id)
        return my_loan_list

    def need_viewed_list(self):
        my_need_list = []
        for need in ViewedNeedNotification.objects.filter(notification_id=self.id).all():
            my_need_list.append(need.need_id)
        return my_need_list

    def invest_viewed_list(self):
        my_invest_list = []
        for invest in ViewedInvestmentNotification.objects.filter(notification_id=self.id).all():
            my_invest_list.append(invest.investment_id)
        return my_invest_list

    def member_viewed_list(self):
        my_member_list = []
        for member in ViewedMembershipNotification.objects.filter(notification_id=self.id).all():
            my_member_list.append(member.mem_request_id)
        return my_member_list


class ViewedLoanNotification(models.Model):
    loan = models.OneToOneField(Loan, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)


class ViewedMembershipNotification(models.Model):
    mem_request = models.OneToOneField(MembershipRequest, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)


class ViewedNeedNotification(models.Model):
    need = models.OneToOneField(Need, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)


class ViewedInvestmentNotification(models.Model):
    investment = models.OneToOneField(Investment, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
