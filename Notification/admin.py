from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Notification)
admin.site.register(ViewedLoanNotification)
admin.site.register(ViewedInvestmentNotification)
admin.site.register(ViewedMembershipNotification)
admin.site.register(ViewedNeedNotification)