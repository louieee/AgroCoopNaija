from django.db import models
from django.conf import settings
from core.models import User
from Lists import Tag


class Reaction(models.Model):
    reaction_choice = (('L', 'Like'), ('D', 'Dislike'), ('N', 'None'))
    type_choice = (('P', 'Post'), ('C', 'Comment'), ('R', 'Reply'), ('N', 'None'))
    reaction = models.CharField( max_length=7,  default='N', choices=reaction_choice)
    message_type = models.CharField(max_length=8, default='N', choices=type_choice)
    message_id = models.IntegerField()
    reactor_id = models.IntegerField()

    def reactor(self):
        return User.objects.get(id=self.reactor_id)


# Create your models here.
class Post(models.Model):
    author_id = models.IntegerField()
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

    def author_detail(self):
        return User.objects.get(id=self.author_id)

    def format_date(self):
        return self.date_posted

    def all_comments(self):
        return Comment.objects.all().filter(post_id=self.id)

    def no_of_comments(self):
        return len(self.all_comments())

    def likes(self):
        return Reaction.objects.filter(reaction='L').filter(message_type='P').filter(message_id=self.id).all()

    def dislikes(self):
        return Reaction.objects.filter(reaction='D').filter(message_type='P').filter(message_id=self.id).all()
    def attachments(self):
        return Attachment.objects.filter(post_id=self.id).all()


class Comment(models.Model):
    author_id = models.IntegerField()
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_posted = models.DateTimeField()

    def all_replies(self):
        return Reply.objects.all().filter(comment_id=self.id)

    def no_of_replies(self):
        return len(self.all_replies())

    def author_detail(self):
        return User(pk=self.author_id)

    def likes(self):
        return Reaction.objects.filter(reaction='L').filter(message_type='C').filter(message_id=self.id).all()

    def dislikes(self):
        return Reaction.objects.filter(reaction='D').filter(message_type='C').filter(message_id=self.id).all()


class Reply(models.Model):
    author_id = models.IntegerField()
    content = models.TextField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    date_posted = models.DateTimeField()

    def author_details(self):
        return User.objects.get(id=self.author_id)

    def likes(self):
        return Reaction.objects.filter(reaction='L').filter(message_type='R').filter(message_id=self.id).all()

    def dislikes(self):
        return Reaction.objects.filter(reaction='D').filter(message_type='R').filter(message_id=self.id).all()


class Attachment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachment/')

