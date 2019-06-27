from django.db import models
from django.conf import settings
from core.models import User
from post.models import Post


# Create your models here.
class Partner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, primary_key=id)
    icon = models.ImageField(upload_to='image/', default='/')
    maximum_degree = models.CharField(max_length=125, default='No Degree')
    specialization = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    position = models.CharField(max_length=255, default='Staff')
    biography = models.TextField()
    verified = models.BooleanField(default=False)
    website = models.URLField()

    def __str__(self):
        return self.institution

    def all_posts(self):
        return Post.objects.all().filter(author_id=self.user_id, for_cooperative=False)

    def user_detail(self):
        return User.objects.get(id=self.user_id)

    def format_specialization(self):
        return self.specialization
