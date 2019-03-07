from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from core.models import User
from product.models import Order
from product.models import Product
from django.conf import settings
import django.utils.timezone
from django.db.models import F


# Create your views here.
def products(request):
    o = Order()
    o.date_ordered = django.utils.timezone.datetime.now()
    time = o.date_ordered
    o.customer = request.user
    o.save()
    products_ = Product.objects.order_by('order__date_ordered').all()
    return render(request, 'product/products.html', {'products': products_, 'time': time})


def product_detail(request, id_):
    product = get_object_or_404(Product, pk=id_)
    return render(request, '../product/templates/product/product_detail.html', {'product': product})


def order_product(request, id_, time):
    user = get_object_or_404(settings.AUTH_USER_MODEL, email=request.user.email)
    if request.method == 'POST':
        cart_ = get_object_or_404(Order, customer=user.id, date_ordered=time)
        product = get_object_or_404(Product, pk=id_)
        product.order = cart_.id
        product.save()
        return redirect('product_detail', id_)
