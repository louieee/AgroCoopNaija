from django.db import models
from cooperative.models import Cooperative
from django.conf import settings


# Create your models here.


class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField()
    delivered = models.BooleanField(default=False)


class Product(models.Model):
    price = models.DecimalField(default=0.0, decimal_places=2, max_digits=50)
    details = models.TextField()
    name = models.CharField(max_length=255)
    # insert tag field here
    image = models.ImageField(upload_to='image/')
    coop = models.ForeignKey(Cooperative, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
