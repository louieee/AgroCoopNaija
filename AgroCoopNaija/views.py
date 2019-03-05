from django.shortcuts import render
from post.models import Post


def home(request):
    posts = Post.objects.order_by('date_posted').filter(coop_name='C').all()
    return render(request, 'core/home.html', {'posts': posts})


def about(request):
    return render(request, 'core/about.html')
