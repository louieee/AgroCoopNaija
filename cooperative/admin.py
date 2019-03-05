from django.contrib import admin
from cooperative.models import Cooperative, Member, Document

# Register your models here.
admin.site.register(Cooperative)
admin.site.register(Member)
admin.site.register(Document)
