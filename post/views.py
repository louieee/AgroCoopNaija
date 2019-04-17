from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from post.models import Post, Comment, Attachment
from cooperative.models import Member
from django.utils import timezone
from django.contrib import auth


# Create your views here.
def make_post(request):
    if request.method == 'POST':
        title = request.POST.get('title', False)
        image = request.FILES.get('image', False)
        video = request.FILES.get('video', False)
        audio = request.FILES.get('audio', False)
        description = request.POST.get('desc', False)
        for_coop = request.POST.get('for_coop', False)
        if title and description:
            new_post = Post()
            new_post.title = title
            new_post.author = auth.get_user_model
            new_post.date_posted = timezone.datetime.now
            new_post.content = description
            if image:
                new_post.image = image
            elif video:
                new_post.video = video
            elif audio:
                new_post.audio = audio
            if for_coop is True:
                new_post.for_coop = True
                member = Member.objects.get(email=auth.get_user)
                new_post.coop_name = member.cooperative.name
            else:
                pass
            new_post.save()
            return redirect('make_post', {'message': 'Your post has been uploaded', 'status': 'success'})
        else:
            return render(request, 'post/make_post.html', {'message': 'All fields must be filled', 'status': 'danger'})

    return render(request, 'post/make_post.html')


def post_detail(request):
    # post = get_object_or_404(Post)
    # attach = get_list_or_404(Attachment, name=post.title)
    # comments = get_list_or_404(Comment, post=post)
    return render(request, 'post/post_detail.html')
                  # {'post': post, 'attach': attach, 'comments': comments})


def comment_detail(request):
    return render(request, 'post/Comment_Detail.html')


