from django.urls import path
from cooperative import views


urlpatterns = [
    path('be_a_member/', views.be_coop_member, name='be_member'),
    path('create/', views.create_coop, name='create_coop'),
    path('all/', views.all_cooperatives, name='all_cooperatives'),
    path('dashboard/', views.dashboard_coop, name='dashboard_coop'),
]