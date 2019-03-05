from django.urls import path
from wallet import views


urlpatterns = [
    path('<name>/', views.wallet, name='wallet'),
    ]
