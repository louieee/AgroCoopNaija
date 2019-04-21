from django.shortcuts import render
from post.models import Post
from partner.models import Partner


def home(request):
    posts = Post.objects.order_by('date_posted').filter(for_cooperative=False).all()
    partners = Partner.objects.all()
    return render(request, 'core/home.html', {'posts': posts, 'partners': partners})


def about(request):
    return render(request, 'core/about.html')

