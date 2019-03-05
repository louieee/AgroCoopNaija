from django.db import models
from wallet.models import Wallet


# Create your models here.
class Cooperative(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    Area_of_Specialization = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image/')
    website = models.URLField()
    email = models.EmailField()
    about = models.TextField()
    wallet = models.OneToOneField(Wallet, on_delete=models.DO_NOTHING)


class Member(models.Model):
    email = models.EmailField(blank=True)
    date_of_birth = models.DateField()
    time_of_request = models.DateTimeField()
    date_of_admission = models.DateTimeField(blank=True)
    cooperative = models.OneToOneField(Cooperative, on_delete=models.CASCADE)


class Document(models.Model):
    desc = models.CharField(max_length=255)
    file = models.FileField(upload_to='document/')
    coop = models.ForeignKey(Cooperative, on_delete=models.CASCADE)
