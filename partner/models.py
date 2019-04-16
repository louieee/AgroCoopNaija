from django.db import models
from django.conf import settings
import re
from core.models import Tag
from post.models import Post


# Create your models here.
class Partner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, primary_key=id)
    image = models.ImageField(upload_to='images/')
    corporate_name = models.CharField(max_length=255)
    biography = models.TextField()
    verified = models.BooleanField(default=False)
    specialization = models.CharField(max_length=255)
    website = models.URLField()

    def __str__(self):
        return self.corporate_name

    def specializations(self):
        ma_list = re.split(";", self.specialization)
        d_list = []
        for b in ma_list:
            d_list.append(Tag(id=int(b)).name)
        return d_list

    def all_posts(self):
        return Post.objects.all().filter(author_id=self.user_id, for_cooperative=False)
