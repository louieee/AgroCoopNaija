from django.urls import path
from cooperative import views


urlpatterns = [
    path('join/request/<int:id_>/', views.be_coop_member, name='join_coop'),
    path('create/', views.create_coop, name='create_coop'),
    path('all/?page=<int:page>/', views.all_cooperatives, name='all_cooperatives'),
    path('<int:_id>/', views.coop_detail, name='coop_detail'),
    path('loan/validate/<int:id_>', views.validate_loan, name='validate_loan'),
    path('investment/validate/<int:id_>/<int:action>/', views.validate_investment, name='validate_investment'),
    path('membership-request/<int:id_>/<int:action>/', views.react_to_membership_request, name='react_request'),
    path('<int:id_>/all-membership-requests/?page=<int:page>/', views.all_membership_requests, name='all_membership'),
    path('<int:id_>/all-new-loans/', views.all_loans, name='all_loans'),
    path('<int:id_>/all-new-needs/?page=<int:page>/', views.all_needs, name='all_needs'),
    path('<int:id_>/all-new-investments/', views.all_investments, name='all_investments'),
    path('add-loan/', views.add_loan, name='add_loan'),
    path('add-investment/<int:id_>/', views.add_investment, name='add_investment'),
    path('add-need/', views.add_need, name='add_need'),
    path('<coop_name>/investment/<int:id_>/', views.investment_detail, name='investment_detail'),
    path('<coop_name>/loan/<int:id_>/', views.loan_detail, name='loan_detail'),
    path('<coop_name>/need/<int:id_>/', views.need_detail, name='need_detail'),
    path('<coop_name>/membership_request/<int:id_>', views.membership_request_detail, name='membership_request_detail'),
    path('<coop_name>/members/?page=<int:page>/', views.all_members, name='all_members'),
    path('<need_title>/investments/?page=<int:page>/', views.all_investors, name='all_investors'),
    path('<int:id_>/all_posts/?page=<int:page>/', views.all_coop_post, name='all_coop_post'),
    path('<int:coop_id>/documents/all/?page=<int:page>/', views.all_documents, name='all_documents'),
    path('<int:coop_id>/documents/add/', views.add_documents, name='add_document'),
    path('<int:coop_id>/Member/<int:id_>/update/?page=<int:page>/', views.update_member, name='update'),
    path('check_cooperative/name=<name>/', views.check_coop_name),
    path('check_cooperative/email=<email>/', views.check_coop_email)
]