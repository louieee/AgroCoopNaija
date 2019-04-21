from django.urls import path
from core import views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.sign_up, name='sign_up'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/user/<int:id_>/', views.profile, name='profile')
]