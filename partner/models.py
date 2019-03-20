from django.db import models
from django.conf import settings
import re
from core.models import Tag


# Create your models here.
class Partner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, primary_key=id)
    image = models.ImageField(upload_to='image/')
    corporate_name = models.CharField(max_length=255)
    biography = models.TextField()
    verified = models.BooleanField(default=False)
    specialization = models.CharField(max_length=255)
    website = models.URLField()

    def tags(self):
        ma_list = re.split(";", self.specialization)
        d_list =[]
        for b in ma_list:
            d_list.append(Tag(id=int(b)).name)
        return d_list

