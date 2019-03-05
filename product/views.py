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
    o.customer = auth.get_user_model()
    o.save()
    products_ = Product.objects.order_by('order__date_ordered').all()
    return render(request, '../product/templates/product/products.html', {'products': products_, 'time': time})


def product_detail(request, id_):
    product = get_object_or_404(Product, pk=id_)
    return render(request, '../product/templates/product/product_detail.html', {'product': product})


def order_product(request, id_):
    if request.method == 'POST':
        cart_ = get_object_or_404(Order, customer=get_object_or_404(settings.AUTH_USER_MODEL,
                                                                    email=User.email))
        product = get_object_or_404(Product, pk=id_)
        cart_.total = F('total') + product.price
        cart_.products.add(product)
        cart_.save()
        return redirect('product_detail', id_)
