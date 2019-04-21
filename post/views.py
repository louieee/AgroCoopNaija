from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from post.models import Post, Comment, Attachment, Reply
from cooperative.models import Member
from django.utils import timezone
from core.models import User


# Create your views here.
def make_post(request):
    if request.method == 'POST':
        title = str(request.POST.get('title', False))
        image = request.FILES.get('image', False)
        video = str(request.POST.get('video', False))
        audio = str(request.POST.get('audio', False))
        description = str(request.POST.get('content', False))
        for_coop = str(request.POST.get('for_coop', False))
        count = 0
        attachments = []
        while request.FILES.get('attachment' + str(count), False) is not False:
            attachments.append(request.FILES.get('attachment' + str(count), False))
            count = count + 1
        if title and description:
            new_post = Post()
            new_post.title = title
            new_post.author = User.objects.get(id=request.user.id)
            new_post.date_posted = timezone.datetime.now()
            new_post.content = description
            if image:
                new_post.image = image
            if video:
                new_post.video = video
            if audio:
                new_post.audio = audio
            if for_coop is True:
                new_post.for_coop = True
                member = Member.objects.get(email=request.user.email)
                new_post.coop_name = member.cooperative.name
            new_post.save()
            for val in attachments:
                new_attachment = Attachment()
                new_attachment.post = new_post
                new_attachment.file = val
                new_attachment.save()

            return render(request, 'post/make_post.html',
                          {'message': 'Your post has been uploaded', 'status': 'success'})
        else:
            return render(request, 'post/make_post.html', {'message': 'All fields must be filled', 'status': 'danger'})

    return render(request, 'post/make_post.html')


def post_detail(request, id_):
    post = Post.objects.get(id=id_)
    rel_post = Post.objects.order_by('-date_posted').filter(tag=post.tag, for_cooperative__exact=False).all()[:10]
    if request.method == 'POST':
        content = str(request.POST.get('content', False))
        if content:
            comment = Comment()
            comment.date_posted = timezone.now()
            comment.author = User(pk=request.user.id)
            comment.content = content
            comment.post = post
            comment.save()
            return render(request, 'post/post_detail.html',
                          {'post': post, 'related': rel_post, 'message': 'Your comment has been sent',
                           'status': 'success'})
        else:
            return render(request, 'post/post_detail.html',
                          {'post': post, 'related': rel_post, 'message': 'Your comment must not be empty',
                           'status': 'danger'})

    return render(request, 'post/post_detail.html',
                  {'post': post, 'related': rel_post})


def comment_detail(request, post_id, id_):
    comment = Comment.objects.get(id=id_, post_id=post_id)
    if request.method == 'POST':
        content = str(request.POST.get('content', False))
        if content:
            reply = Reply()
            reply.content = content
            reply.comment = comment
            reply.author = User(pk=request.user.id)
            reply.date_posted = timezone.now()
            reply.save()
            return render(request, 'post/Comment_Detail.html', {'comment': comment, 'message': 'Your reply has been '
                                                                                               'sent',
                                                                'status': 'success'})
        else:
            return render(request, 'post/Comment_Detail.html',
                          {'comment': comment, 'message': 'You cannot send an empty reply',
                           'status': 'danger'})
    return render(request, 'post/Comment_Detail.html', {'comment': comment})
