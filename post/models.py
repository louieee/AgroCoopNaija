from django.db import models
from django.conf import settings


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    date_posted = models.DateTimeField()
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image/', blank=True)
    video = models.FileField(upload_to='video/', blank=True)
    audio = models.FileField(upload_to='audio/', blank=True)
    for_coop = models.BooleanField(default=False)
    coop_name = models.CharField(max_length=255, blank=True)
    content = models.TextField()


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_posted = models.DateTimeField()


class Reply(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    date_posted = models.DateTimeField()


class Attachment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachment/')
