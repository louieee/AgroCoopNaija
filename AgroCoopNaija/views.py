from django.shortcuts import render
from post.models import Post
from partner.models import Partner
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests


def connected_to_internet():
    try:
        _ = requests.get('https://forecast7.com/en/6d467d55/enugu/', timeout=5)
        return True
    except requests.ConnectionError:
        return False


def home(request):
    posts = Post.objects.order_by('-date_posted').filter(for_cooperative=False).all()[:10]
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    return render(request, 'core/home.html', {'posts': posts, 'pages': pages, 'internet': connected_to_internet()})


# This view returns the about me page
def about(request):
    return render(request, 'core/about.html')


# This view returns the error 400 page
def handler404(request):
    return render(request, '404.html', status=404)


# This view returns the error 500 page
def handler500(request):
    return render(request, '500.html', status=500)
