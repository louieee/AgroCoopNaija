from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    is_coop_member = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/')


class Tag(models.Model):
    name = models.CharField(max_length=255, primary_key=True)


class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.DO_NOTHING)
    acct_name = models.CharField(max_length=255)
    acct_number = models.CharField(max_length=255)
    balance = models.DecimalField(default=0.0, decimal_places=2, max_digits=50)


class Cooperative(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    default_password = models.CharField(max_length=255)
    Area_of_Specialization = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to='image/')
    website = models.URLField()
    email = models.EmailField()
    about = models.TextField()
    wallet = models.OneToOneField(Wallet, on_delete=models.DO_NOTHING)


class Member(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, primary_key=True)
    date_of_birth = models.DateField()
    date_of_admission = models.DateTimeField()
    username = models.CharField(max_length=50)
    cooperative = models.OneToOneField(Cooperative, on_delete=models.CASCADE)
    password = models.CharField(max_length=255)


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, primary_key=True)
    phone_no = models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)


class Partner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, primary_key=True)
    corporate_name = models.CharField(max_length=255)
    biography = models.TextField()
    institution = models.CharField(max_length=255)
    website = models.URLField()
    password = models.CharField(max_length=255)


class Attachment(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    file = models.FileField(upload_to='attachment/')


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    content = models.TextField()
    date_posted = models.DateTimeField(default=None)
    replies = models.ManyToManyField("self", blank=True)


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    date_posted = models.DateTimeField()
    title = models.CharField(max_length=255)
    coop_name = models.CharField(max_length=255, blank=True)
    corporate_name = models.CharField(max_length=255, blank=True)
    attachments = models.ManyToManyField(Attachment, blank=True)
    comments = models.ManyToManyField(Comment, blank=True)
    content = models.TextField()


class Product(models.Model):
    price = models.DecimalField(default=0.0, decimal_places=2, max_digits=50)
    details = models.TextField()
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image/')
    coop = models.ForeignKey(Cooperative, on_delete=models.CASCADE)


class Order(models.Model):
    tracking_no = models.CharField(max_length=255, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField()
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(default=0.0, decimal_places=2, max_digits=50)
    delivered = models.BooleanField(default=False)


class Transaction(models.Model):
    sender = models.ForeignKey(Wallet, related_name='sender', on_delete=models.DO_NOTHING)
    receiver = models.ForeignKey(Wallet, related_name='receiver', on_delete=models.DO_NOTHING)
    detail = models.TextField()
    amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=50)
