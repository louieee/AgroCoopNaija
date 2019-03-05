from django.db import models
from django.conf import settings


# Create your models here.
class Partner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    corporate_name = models.CharField(max_length=255)
    biography = models.TextField()
    institution = models.CharField(max_length=255)
    website = models.URLField()
