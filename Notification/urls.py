from django.urls import path
from . import views


urlpatterns = [
    path('investment/<int:id_>/', views.add_to_invest_list, name='add_viewed_invest'),
    path('loan/<int:id_>/', views.add_to_loan_list, name='add_viewed_loan'),
    path('need/<int:id_>/', views.add_to_need_list, name='add_viewed_need'),
    path('membership-request/<int:id_>/', views.add_to_member_list, name='add_viewed_member')
    ]
