from django.urls import path
from core import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.sign_up, name='sign_up'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/user/<int:id_>/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/Settings/', views.user_setting, name='settings'),
    path('check_email/email=<email>/', views.email_exist, name='email_exist'),
    path('check_username/username=<username>/', views.username_exist, name='username_exist')
]
