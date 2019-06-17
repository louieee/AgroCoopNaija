from django.shortcuts import render
from post.models import Post
from partner.models import Partner

import requests


def connected_to_internet():
    try:
        _ = requests.get('https://forecast7.com/en/6d467d55/enugu/', timeout=5)
        return True
    except requests.ConnectionError:
        return False


def home(request):
    posts = Post.objects.order_by('date_posted').filter(for_cooperative=False).all()
    partners = Partner.objects.all()
    return render(request, 'core/home.html', {'posts': posts, 'partners': partners, 'internet': connected_to_internet()})


def about(request):
    return render(request, 'core/about.html')
