from django.urls import path
from product import views


urlpatterns = [
    path('<int:id>/', views.product_detail, name='product_detail'),
    path('all/', views.products, name='products'),
    path('order/', views.order_product, name='order_product')
    ]
