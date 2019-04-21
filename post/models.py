from django.db import models
from django.conf import settings
from core.models import User
from Lists import Tag


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    date_posted = models.DateTimeField()
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image/', blank=True)
    video = models.URLField(blank=True)
    tag = models.CharField(max_length=255, default=Tag.tags[1])
    audio = models.URLField(blank=True)
    for_cooperative = models.BooleanField(default=False)
    cooperative_name = models.CharField(max_length=255, blank=True)
    content = models.TextField()

    def post_summary(self):
        return self.content[:100]

    def author_name(self):
        return self.author

    def format_date(self):
        return self.date_posted

    def all_comments(self):
        return Comment.objects.all().filter(post_id=self.id)

    def no_of_comments(self):
        return len(self.all_comments())


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_posted = models.DateTimeField()

    def all_replies(self):
        return Reply.objects.all().filter(comment_id=self.id)

    def no_of_replies(self):
        return len(self.all_replies())


class Reply(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    date_posted = models.DateTimeField()

    def author_details(self):
        return User.objects.get(username=self.author)


class Attachment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachment/')
