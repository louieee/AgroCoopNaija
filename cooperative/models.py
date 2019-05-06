from django.db import models
from django.conf import settings
from decimal import Decimal
from django.contrib.auth.models import Group
import django.utils.timezone
from post.models import Post
from core.models import User


# Create your models here.
class Cooperative(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    Area_of_Specialization = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='image/')
    website = models.URLField()
    motto = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=50, default='')
    email = models.EmailField()
    about = models.TextField()
    reg_no = models.CharField(max_length=100, default='')
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    bank = models.CharField(max_length=255)

    def all_members(self):
        return Member.objects.all().filter(cooperative_id=self.id)

    def all_posts(self):
        return Post.objects.all().filter(cooperative_name=self.name)

    def all_needs(self):
        return Need.objects.all().filter(cooperative_id=self.id)

    def all_unpaid_loans(self):
        return Loan.objects.all().filter(borrower__cooperative_id=self.id, paid=False, status='G')

    def all_new_loans(self):
        return Loan.objects.all().filter(borrower__cooperative_id=self.id, paid=False, status='N')

    def __str__(self):
        return self.name

    def membership_requests(self):
        return MembershipRequest.objects.all().filter(cooperative_id=self.id)

    def all_new_investments(self):
        return Investment.objects.all().filter(cooperative_id=self.id, verified=None)


class MembershipRequest(models.Model):
    sender_id = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    time_of_request = models.DateTimeField()
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name) + 'requests to become a member '

    def sender_detail(self):
        return User.objects.get(id=self.sender_id)


class Member(models.Model):
    roles = (('Committee Member', 'Committee Member'), ('Member', 'Member'))
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=id)
    time_of_request = models.DateTimeField()
    date_of_admission = models.DateTimeField(blank=True)
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, default='Member', choices=roles)

    def cooperative_posts(self):
        return Post.objects.all().filter(author_id=self.user_id, for_cooperative=True,
                                         cooperative_name=self.cooperative.name)

    def general_posts(self):
        return Post.objects.all().filter(author_id=self.user_id, for_cooperative=False)

    def paid_loans(self):
        return Loan.objects.all().filter(borrower__cooperative_id=self.cooperative.id, borrower_id=self.id, paid=True,
                                         status='G')

    def unpaid_loans(self):
        return Loan.objects.all().filter(borrower__cooperative_id=self.cooperative.id, borrower_id=self.id, paid=False,
                                         status='G')

    def unverified_loans(self):
        return Loan.objects.all().filter(borrower__cooperative_id=self.cooperative.id, borrower_id=self.id,
                                         paid=False, status='N')

    def declined_loans(self):
        return Loan.objects.all().filter(borrower__cooperative_id=self.cooperative.id, borrower_id=self.id,
                                         paid=False, status='D')

    def verified_investments(self):
        return Investment.objects.all().filter(investor_id=self.id, investor__cooperative_id=self.cooperative.id,
                                               verified=True)

    def unverified_investments(self):
        return Investment.objects.all().filter(investor_id=self.id, investor__cooperative_id=self.cooperative.id,
                                               verified=None)

    def false_investments(self):
        return Investment.objects.all().filter(investor_id=self.id, investor__cooperative_id=self.cooperative.id,
                                               verified=False)


class Document(models.Model):
    desc = models.CharField(max_length=255)
    file = models.FileField(upload_to='document/')
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)

    def __str__(self):
        return self.desc


class Need(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    amount = models.DecimalField(decimal_places=2, max_digits=50)
    time = models.DateTimeField()
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)

    def all_investments(self):
        return Investment.objects.all().filter(need_id=self.id, investor__cooperative=self.cooperative)

    def __str__(self):
        return self.title

    def format_date(self):
        return self.time


class Loan(models.Model):
    status_choice = (('N', 'New'), ('G', 'Granted'), ('D', 'Declined'))
    amount = models.DecimalField(decimal_places=2, max_digits=50)
    status = models.CharField(max_length=10, default='N', choices=status_choice)
    paid = models.BooleanField(default=False)
    time_asked = models.DateTimeField()
    time_granted = models.DateTimeField()
    time_to_pay = models.DateTimeField()
    percentage_of_interest = models.DecimalField(default=0.00, decimal_places=2, max_digits=50)
    borrower = models.ForeignKey(Member, on_delete=models.CASCADE)

    def amount_to_pay(self):
        return Decimal(self.amount) + (Decimal(self.amount) * (Decimal(self.percentage_of_interest) / 100))

    def all_collateral(self):
        return Collateral.objects.all().filter(Loan_id=self.id)

    def borrower_detail(self):
        return User.objects.get(id=self.borrower_id)


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
    amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=50)
    payment_proof = models.ImageField(upload_to='image/')
    verified = models.BooleanField(default=None)
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return 'Investment For ' + self.need.title + 'By ' + self.investor.user.name

    def share(self):
        return (Decimal(self.amount) / Decimal(self.need.amount)) * 100

    def need_detail(self):
        return Need.objects.get(id=self.need_id).title

    def investor_detail(self):
        return User.objects.get(id=self.investor)
