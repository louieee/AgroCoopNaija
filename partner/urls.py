from django.urls import path
from partner import views


urlpatterns = [
    path('<int:id>/', views.partner_detail, name='partner_detail'),
    path('all/', views.all_partners, name='all_partners'),
    path('be_a_partner/', views.be_partner, name='be_partner'),
    path('dashboard/', views.dashboard_partner, name='dashboard_partner'),
]