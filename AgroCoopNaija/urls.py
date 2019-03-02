"""AgroCoopNaija URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('add_to_cart/', views.cart, name='add_to_cart'),
    path('about/', views.about, name='about'),
    path('wallet/', views.wallet, name='wallet'),
    path('products/', views.products, name='products'),
    path('product_detail/', views.product_detail, name='product_detail'),
    path('post_detail/', views.post_detail, name='post_detail'),
    path('partner_login/', views.partner_login, name='partner_login'),
    path('partner_detail/', views.partner_detail, name='partner_detail'),
    path('make_post/', views.make_post, name='make_post'),
    path('dashboard/partner/', views.dashboard_partner, name='dashboard_partner'),
    path('dashboard_customer/', views.dashboard_Customer, name='Dashboard_Customer'),
    path('customer_login/', views.customer_login, name='customer_login'),
    path('dashboard_coop/', views.Dashboard_coop, name='Dashboard_coop'),
    path('create_coop/', views.create_coop, name='create_coop'),
    path('coop_login/', views.coop_login, name='coop_login'),
    path('be_partner/', views.be_partner, name='be_partner'),
    path('be_customer/', views.be_customer, name='be_customer'),
    path('all_partners/', views.all_partners, name='all_partners'),
    path('all_cooperatives/', views.all_cooperatives, name='all_cooperatives'),

    path(r'^logout/$', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
