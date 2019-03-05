from django.contrib import admin
from post import models

# Register your models here.
admin.site.register(models.Comment)
admin.site.register(models.Post)
admin.site.register(models.Attachment)
admin.site.register(models.Reply)
