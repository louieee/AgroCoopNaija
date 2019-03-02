from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.conf import settings
from django.utils.timezone import datetime as datetime
from django.contrib.auth.hashers import MD5PasswordHasher as hasher
from core import models
from django.db.models import F


def about(request):
    return render(request, 'about.html')


def all_cooperatives(request):
    all_coop = models.Cooperative().objects.all()
    return render(request, 'all_cooperatives.html', {'cooperative': all_coop})


def all_partners(request):
    partners = models.Partner().objects.all()
    return render(request, 'all_partners.html', {'partners': partners})


def be_customer(request):
    return render(request, 'be_customer.html')


def be_partner(request):
    return render(request, 'be_partner.html')


def coop_login(request):
    return render(request, 'coop_login.html')


def create_coop(request):
    return render(request, 'create_coop.html')


def customer_login(request):
    return render(request, 'customer_login.html')


def Dashboard_coop(request, username):
    member = get_object_or_404(models.Member, username=username)
    name = member.cooperative.name
    orders = models.Order().objects.get(products__coop=member.cooperative).objects.all()
    posts = models.Post.objects.order_by('date_posted').get(coop_name=name).objects.all()
    return render(request, 'Dashboard-coop.html', {'member': member, 'posts': posts, 'orders': orders})


def dashboard_Customer(request, username):
    customer = get_object_or_404(models.Customer, username=username)
    m_wallet = get_object_or_404(models.Wallet, user=customer.user)
    transactions = get_list_or_404(models.Transaction, sender=m_wallet)
    orders = get_list_or_404(models.Order, customer=customer)
    return render(request, 'Dashboard-Customer.html', {'customer': customer, 'wallet': m_wallet,
                                                       'transactions': transactions, 'orders': orders})


def dashboard_partner(request, username):
    partner = get_object_or_404(models.Partner, username=username)
    posts = get_list_or_404(models.Post, author=partner.user)
    return render(request, 'Dashboard-partner.html', {'partner': partner, 'posts': posts})


def home(request):
    posts = models.Post().objects.order_by('date_posted').get(coop_name__isnull=True).objects.all()
    return render(request, 'home.html', {'posts', posts})


def make_post(request):
    return render(request, 'make_post.html')


def partner_detail(request, username):
    partner = get_object_or_404(models.Partner, username=username)
    return render(request, 'partner_detail.html', {'partner': partner})


def partner_login(request):
    return render(request, 'partner_login.html')


def post_detail(request, id_):
    post = get_object_or_404(models.Post, pk=id_)
    return render(request, 'post_detail.html', {'post', post})


def products(request):
    o = models.Order()
    o.date_ordered = datetime.now()
    time = o.date_ordered
    o.customer = get_object_or_404(models.Customer, user=auth.get_user)
    o.save()
    products_ = models.Product.objects.order_by('order__date_ordered').all()
    return render(request, 'products.html', {'products': products_, 'time': time})


def product_detail(request, id_):
    product = get_object_or_404(models.Product, pk=id_)
    return render(request, 'product_detail.html', {'product': product})


def wallet(request, email):
    wallet_ = get_object_or_404(models.Wallet, user=get_object_or_404(settings.AUTH_USER_MODEL, email=email))
    return render(request, 'wallet.html', {'wallet': wallet_})


def cart(request, id_):
    if request.method == 'POST':
        cart_ = get_object_or_404(models.Order, customer=get_object_or_404(models.Customer, user=auth.get_user))
        product = get_object_or_404(models.Product, pk=id_)
        cart_.total = F('total') + product.price
        cart_.products.add(product)
        cart_.save()
        return redirect('product_detail', id_)
