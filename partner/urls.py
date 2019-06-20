from django.urls import path
from partner import views


urlpatterns = [
    path('<int:id_>/', views.partner_detail, name='partner_detail'),
    path('all/?page=<int:page>/', views.all_partners, name='all_partners'),
    path('join/', views.be_partner, name='be_partner'),
]