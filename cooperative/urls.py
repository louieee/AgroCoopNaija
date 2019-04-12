from django.urls import path
from cooperative import views


urlpatterns = [
    path('join/', views.be_coop_member, name='join_coop'),
    path('create/', views.create_coop, name='create_coop'),
    path('all/', views.all_cooperatives, name='all_cooperatives'),
    path('dashboard/', views.dashboard_coop, name='dashboard_coop'),
    path('<int:_id>/', views.coop_detail, name='coop_detail')
]