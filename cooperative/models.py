from django.db import models
from django.conf import settings
from decimal import Decimal
from django.contrib.auth.models import Group
from post.models import Post as Post
from core.models import User


# Create your models here.
class Cooperative(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    address = models.CharField(max_length=255, default='')
    Area_of_Specialization = models.CharField(max_length=255)
    no_of_shares = models.PositiveIntegerField(default=0)
    icon = models.ImageField(upload_to='image/', default='/')
    website = models.URLField()
    motto = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=50, default='')
    email = models.EmailField()
    about = models.TextField()
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    bank = models.CharField(max_length=255)

    def all_members(self):
        return Member.objects.all().filter(cooperative_id=self.id).order_by('date_of_admission')

    def members(self):
        list_ = []
        for member in self.all_members():
            list_.append(member.user_id)
        return list_

    def all_posts(self):
        return Post.objects.order_by('-date_posted').all().filter(cooperative_name=self.name)

    def all_needs(self):
        return Need.objects.all().filter(cooperative_id=self.id).order_by('-id')

    def all_unpaid_loans(self):
        return Loan.objects.all().filter(borrower__cooperative_id=self.id, paid=False, status='G')

    def all_declined_loans(self):
        return Loan.objects.all().filter(borrower__cooperative_id=self.id, paid=False, status='D')

    def all_paid_loans(self):
        return Loan.objects.all().filter(borrower__cooperative_id=self.id, paid=True, status='G')

    def all_new_loans(self):
        return Loan.objects.all().filter(borrower__cooperative_id=self.id, paid=False, status='N')

    def all_loans(self):
        return Loan.objects.all().filter(borrower__cooperative_id=self.id).order_by('-id')

    def all_investments(self):
        return Investment.objects.all().filter(cooperative_id=self.id).order_by('-id')

    def __str__(self):
        return self.name

    def membership_requests(self):
        return MembershipRequest.objects.all().filter(cooperative_id=self.id).order_by('-id')

    def all_new_investments(self):
        return Investment.objects.all().filter(cooperative_id=self.id, verified=None)

    def all_false_investments(self):
        return Investment.objects.all().filter(cooperative_id=self.id, verified=False)

    def all_verified_investments(self):
        return Investment.objects.all().filter(cooperative_id=self.id, verified=True)

    def all_documents(self):
        return Document.objects.all().filter(cooperative_id=self.id).order_by('-id')


class MembershipRequest(models.Model):
    sender_id = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    business_plan = models.FileField(default='/')
    letter = models.FileField(default='/')
    motivation = models.TextField(default='')
    time_of_request = models.DateTimeField()
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name) + ' requests to become a member '

    def sender_detail(self):
        return User.objects.get(id=self.sender_id)


class Member(models.Model):
    roles = (('President', 'President'), ('Vice President', 'Vice President'), ('Secretary', 'Secretary'),
             ('Treasurer', 'Treasurer'), ('Floor Member', 'Floor Member'))
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=id)
    time_of_request = models.DateTimeField()
    date_of_admission = models.DateTimeField(blank=True)
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, default='Floor Member', choices=roles)

    def cooperative_posts(self):
        return Post.objects.all().filter(author_id=self.user_id, for_cooperative=True,
                                         cooperative_name=self.cooperative.name).order_by('-id')

    def __str__(self):
        return self.user_detail().first_name + ' - ' + self.coop_detail().name

    def general_posts(self):
        return Post.objects.all().filter(author_id=self.user_id, for_cooperative=False).order_by('-id')

    def paid_loans(self):
        return Loan.objects.all().filter(borrower__cooperative_id=self.cooperative.id, borrower_id=self.user_id,
                                         paid=True,
                                         status='G')

    def unpaid_loans(self):
        return Loan.objects.all().filter(borrower__cooperative_id=self.cooperative.id, borrower_id=self.user_id,
                                         paid=False,
                                         status='G')

    def unverified_loans(self):
        return Loan.objects.all().filter(borrower__cooperative_id=self.cooperative.id, borrower_id=self.user_id,
                                         paid=False, status='N')

    def declined_loans(self):
        return Loan.objects.all().filter(borrower__cooperative_id=self.cooperative.id, borrower_id=self.user_id,
                                         paid=False, status='D')

    def verified_investments(self):
        return Investment.objects.all().filter(investor_id=self.user_id, investor__cooperative_id=self.cooperative.id,
                                               verified=True)

    def unverified_investments(self):
        return Investment.objects.all().filter(investor_id=self.user_id, investor__cooperative_id=self.cooperative.id,
                                               verified=None)

    def false_investments(self):
        return Investment.objects.all().filter(investor_id=self.user_id, investor__cooperative_id=self.cooperative.id,
                                               verified=False)

    def user_detail(self):
        return User.objects.get(id=self.user_id)

    def coop_detail(self):
        return Cooperative.objects.get(id=self.cooperative_id)

    def invested_needs(self):
        return Need.objects.all().filter(investment__investor__user_id=self.user_id)

    def needs_not_invested(self):
        return self.coop_detail().all_needs().count() - self.invested_needs().count()


class Document(models.Model):
    desc = models.CharField(max_length=255)
    file = models.FileField(upload_to='document/')
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)

    def __str__(self):
        return self.desc + ' - ' + self.cooperative.name


class Need(models.Model):
    title = models.CharField(max_length=255)
    purpose = models.TextField()
    amount = models.DecimalField(decimal_places=2, max_digits=50)
    mandated_payment = models.DecimalField(decimal_places=2, max_digits=50, default=0.00)
    time = models.DateTimeField()
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - ' + self.cooperative_().name

    def all_investments(self):
        return Investment.objects.all().filter(need_id=self.id, investor__cooperative=self.cooperative).order_by(
            '-time')

    def investors(self):
        my_list = []
        for investment in self.all_investments():
            my_list.append(investment.investor_detail())
        return my_list

    def cooperative_(self):
        return Cooperative.objects.get(id=self.cooperative_id)

    def format_date(self):
        return self.time


class Loan(models.Model):
    status_choice = (('N', 'New'), ('G', 'Granted'), ('D', 'Declined'))
    amount = models.DecimalField(decimal_places=2, max_digits=50)
    status = models.CharField(max_length=10, default='N', choices=status_choice)
    paid = models.BooleanField(default=False)
    purpose = models.TextField(default='')
    time_asked = models.DateTimeField()
    time_granted = models.DateTimeField(null=True)
    time_to_pay = models.DateTimeField(null=True)
    percentage_of_interest = models.DecimalField(default=0.00, decimal_places=2, max_digits=50)
    borrower = models.ForeignKey(Member, on_delete=models.CASCADE)

    def amount_to_pay(self):
        return Decimal(self.amount) + (Decimal(self.amount) * (Decimal(self.percentage_of_interest) / 100))

    def all_collateral(self):
        return Collateral.objects.all().filter(Loan_id=self.id)

    def borrower_detail(self):
        return User.objects.get(id=self.borrower_id)

    def __str__(self):
        return 'Loan for ' + self.borrower.coop_detail().name + ' - ' + str(self.id)


class Collateral(models.Model):
    title = models.CharField(max_length=255)
    document = models.FileField(upload_to='attachment/')
    verified = models.BooleanField(default=False)
    Loan = models.ForeignKey(Loan, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Investment(models.Model):
    need = models.ForeignKey(Need, on_delete=models.CASCADE)
    investor = models.ForeignKey(Member, on_delete=models.CASCADE)
    time = models.DateTimeField()
    payment_proof = models.ImageField(upload_to='image/')
    verified = models.BooleanField(default=None, null=True)
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return 'Investment for ' + self.investor.coop_detail().name + ' - ' + str(self.id)

    def need_detail(self):
        return Need.objects.get(id=self.need_id)

    def investor_detail(self):
        return User.objects.get(id=self.investor_id)
