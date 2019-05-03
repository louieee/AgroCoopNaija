from django.db import models
from cooperative.models import Member, Cooperative, Loan


# Create your models here.
class Notification(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)

    def loan_display(self):
        coop_id = Member.objects.get(id=self.member_id).cooperative_id
        all_new_loan = Cooperative.objects.get(id=coop_id).all_new_loans.count()
        viewed_loan = ViewedLoanNotification.objects.filter(member__user_id=self.member_id).all().count()
        return int(all_new_loan) - int(viewed_loan)

    def need_display(self):
        coop_id = Member.objects.get(id=self.member_id).cooperative_id
        all_new_need = Cooperative.objects.get(id=coop_id).all_needs.count()
        viewed_need = ViewedNeedNotification.objects.filter(member__user_id=self.member_id).all().count()
        return int(all_new_need) - int(viewed_need)

    def membership_display(self):
        coop_id = Member.objects.get(id=self.member_id).cooperative_id
        new_membership = Cooperative.objects.get(id=coop_id).membership_requests.count()
        viewed_membership = ViewedMembershipNotification.objects.filter(member__user_id=self.member_id).all().count()
        return int(new_membership) - int(viewed_membership)

    def investment_display(self):
        coop_id = Member.objects.get(id=self.member_id).cooperative_id
        new_investment = Cooperative.objects.get(id=coop_id).all_investments.count()
        viewed_investment = ViewedInvestmentNotification.objects.filter(member__user_id=self.member_id).all().count()
        return int(new_investment) - int(viewed_investment)

    def loan_viewed_list(self):
        my_loan_list = []
        for loan in ViewedLoanNotification.objects.filter(member__user_id=self.member_id).all():
            my_loan_list.append(loan.loan_id)
        return my_loan_list

    def need_viewed_list(self):
        my_need_list = []
        for need in ViewedNeedNotification.objects.filter(member__user_id=self.member_id).all():
            my_need_list.append(need.need_id)
        return my_need_list

    def invest_viewed_list(self):
        my_invest_list = []
        for invest in ViewedInvestmentNotification.objects.filter(member__user_id=self.member_id).all():
            my_invest_list.append(invest.investment_id)
        return my_invest_list

    def member_viewed_list(self):
        my_member_list = []
        for member in ViewedMembershipNotification.objects.filter(member__user_id=self.member_id).all():
            my_member_list.append(member.member_id)
        return my_member_list


class ViewedLoanNotification(models.Model):
    loan_id = models.IntegerField()
    member = models.ForeignKey(Member, on_delete=models.CASCADE)


class ViewedMembershipNotification(models.Model):
    membership_id = models.IntegerField()
    member = models.ForeignKey(Member, on_delete=models.CASCADE)


class ViewedNeedNotification(models.Model):
    need_id = models.IntegerField()
    member = models.ForeignKey(Member, on_delete=models.CASCADE)


class ViewedInvestmentNotification(models.Model):
    investment_id = models.IntegerField()
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
