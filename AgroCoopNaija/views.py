from django.shortcuts import render
from post.models import Post
from partner.models import Partner
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests


# This function checks if the system is connected to the internet
# it returns true if its connected to the internet and returns false if otherwise
def connected_to_internet():
    try:
        _ = requests.get('https://forecast7.com/en/6d467d55/enugu/', timeout=5)
        return True
    except requests.ConnectionError:
        return False


# This view gets details renders the homepage and gets general posts from the database and
# renders it onto the home page
def home(request):
    posts = Post.objects.order_by('-date_posted').filter(for_cooperative=False).all()[:10]
    return render(request, 'core/home.html', {'posts': posts, 'internet': connected_to_internet()})


# This view returns the about me page
def about(request):
    return render(request, 'core/about.html')


# This view returns the error 400 page
def handler404(request):
    return render(request, '404.html', status=404)


# This view returns the error 500 page
def handler500(request):
    return render(request, '500.html', status=500)
