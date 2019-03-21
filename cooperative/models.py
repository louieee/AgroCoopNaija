from django.db import models
from django.conf import settings
from decimal import Decimal
from django.contrib.auth.models import Group
import django.utils.timezone
import re
from core.models import Tag
from post.models import Post


# Create your models here.
class Cooperative(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    Area_of_Specialization = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image/')
    website = models.URLField()
    email = models.EmailField()
    about = models.TextField()
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
        return Loan.objects.all().filter(borrower__cooperative_id=self.id, paid=False, granted=True)

    def all_non_granted_loans(self):
        return Loan.objects.all().filter(borrower__cooperative_id=self.id, paid=False, granted=False)

    def __str__(self):
        return self.name

    def list_of_specializations(self):
        ma_list = re.split(";", self.Area_of_Specialization)
        d_list = []
        for b in ma_list:
            d_list.append(Tag(id=int(b)).name)
        return d_list


class Member(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=id)
    date_of_birth = models.DateField()
    time_of_request = models.DateTimeField()
    date_of_admission = models.DateTimeField(blank=True)
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    bank = models.CharField(max_length=255)

    def cooperative_posts(self):
        return Post.objects.all().filter(author_id=self.user_id, for_cooperative=True,
                                         cooperative_name=self.cooperative.name)

    def general_posts(self):
        return Post.objects.all().filter(author_id=self.user_id, for_cooperative=False)

    def loans(self):
        return Loan.objects.all().filter(borrower__cooperative_id=self.cooperative.id, borrower_id=self.id)

    def unpaid_loans(self):
        return Loan.objects.all().filter(borrower__cooperative_id=self.cooperative.id, borrower_id=self.id, paid=False)

    def overdue_loans(self):
        return Loan.objects.all().filter(borrower__cooperative_id=self.cooperative.id, borrower_id=self.id,
                                         paid=False, time_to_pay__lt=django.utils.timezone.datetime.now())

    def investments(self):
        return Investment.objects.all().filter(investor_id=self.id, investor__cooperative_id=self.cooperative.id)


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
    amount = models.DecimalField(decimal_places=2, max_digits=50)
    granted = models.BooleanField(default=False)
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
    verified = models.BooleanField(default=False)

    def __str__(self):
        return 'Investment For ' + self.need.title + 'By ' + self.investor.user.name

    def share(self):
        return (Decimal(self.amount) / Decimal(self.need.amount)) * 100
