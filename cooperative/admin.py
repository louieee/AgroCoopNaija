from django.contrib import admin
from cooperative.models import Cooperative, Member, Document, Need, Loan, Investment, MembershipRequest, Collateral

# Register your models here.
admin.site.register(Cooperative)
admin.site.register(Member)
admin.site.register(Document)
admin.site.register(Loan)
admin.site.register(Need)
admin.site.register(Investment)
admin.site.register(MembershipRequest)
admin.site.register(Collateral)

