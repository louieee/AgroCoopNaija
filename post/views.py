from django.shortcuts import render, redirect, HttpResponse
from post.models import Post, Comment, Attachment, Reply, Reaction
from cooperative.models import Member, Cooperative
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def make_post(request):
    if request.method == 'POST':
        title = str(request.POST.get('title', False))
        image = request.FILES.get('image', False)
        video = str(request.POST.get('video', False))
        audio = str(request.POST.get('audio', False))
        description = str(request.POST.get('content', False))
        for_coop = int(request.POST.get('for_cooperative', False))
        count = 0
        attachments = []
        while request.FILES.get('attachment' + str(count), False) is not False:
            attachments.append(request.FILES.get('attachment' + str(count), False))
            count = count + 1
        if title and description:
            new_post = Post()
            new_post.author_id = request.user.id
            new_post.title = title
            new_post.date_posted = timezone.datetime.now()
            new_post.content = description
            if image:
                new_post.image = image
            if video:
                new_post.video = video
            if audio:
                new_post.audio = audio
            if for_coop == 1:
                new_post.for_cooperative = True
                member = Member.objects.get(user_id=request.user.id)
                new_post.cooperative_name = member.coop_detail().name
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
    rel_post = Post.objects.order_by('-date_posted').filter(tag=post.tag, for_cooperative__exact=False).all()
    page = request.GET.get('page', 1)
    paginator = Paginator(rel_post, 10)
    try:
        rel_pages = paginator.page(page)
    except PageNotAnInteger:
        rel_pages = paginator.page(1)
    except EmptyPage:
        rel_pages = paginator.page(paginator.num_pages)

    page = request.GET.get('page', 1)
    paginator = Paginator(post.all_comments(), 10)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        content = str(request.POST.get('content', False))
        if content:
            comment = Comment()
            comment.author_id = request.user.id
            comment.date_posted = timezone.now()
            comment.content = content
            comment.post = post
            comment.save()
            return redirect('/post/' + str(id_) + '/')
        else:
            return render(request, 'post/post_detail.html',
                          {'post': post, 'related': rel_post, 'rel_pages': rel_pages, 'pages': pages})

    return render(request, 'post/post_detail.html',
                  {'post': post, 'related': rel_post, 'rel_pages': rel_pages, 'pages': pages})


def comment_detail(request, post_id, id_):
    comment = Comment.objects.get(id=id_, post_id=post_id)
    page = request.GET.get('page', 1)
    paginator = Paginator(comment.all_replies(), 10)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        content = str(request.POST.get('content', False))
        if content:
            reply = Reply()
            reply.content = content
            reply.comment = comment
            reply.author_id = request.user.id
            reply.date_posted = timezone.now()
            reply.save()
            return redirect('/post/' + str(post_id) + '/comment/' + str(id_) + '/')
        else:
            return render(request, 'post/Comment_Detail.html',
                          {'comment': comment, 'message': 'You cannot send an empty reply',
                           'status': 'danger', 'pages': pages})
    return render(request, 'post/Comment_Detail.html', {'comment': comment, 'pages': pages})


def who_liked(request, letter, id_):
    if request.method == 'GET':
        if letter == 'Post':
            post = Post.objects.get(id=id_)
            likes = post.likes()
            page = request.GET.get('page', 1)
            paginator = Paginator(likes, 10)
            try:
                pages = paginator.page(page)
            except PageNotAnInteger:
                pages = paginator.page(1)
            except EmptyPage:
                pages = paginator.page(paginator.num_pages)

            return render(request, 'post/Likes.html',
                          {'likes': likes, 'message_obj': post, 'message': letter, 'pages': pages})
        elif letter == 'Comment':
            comment = Comment.objects.get(id=id_)
            likes = comment.likes()
            page = request.GET.get('page', 1)
            paginator = Paginator(likes, 10)
            try:
                pages = paginator.page(page)
            except PageNotAnInteger:
                pages = paginator.page(1)
            except EmptyPage:
                pages = paginator.page(paginator.num_pages)

            return render(request, 'post/Likes.html',
                          {'likes': likes, 'message_obj': comment, 'message': letter, 'pages': pages})
        elif letter == 'Reply':
            reply = Reply.objects.get(id=id_)
            likes = reply.likes()
            page = request.GET.get('page', 1)
            paginator = Paginator(likes, 10)
            try:
                pages = paginator.page(page)
            except PageNotAnInteger:
                pages = paginator.page(1)
            except EmptyPage:
                pages = paginator.page(paginator.num_pages)
            return render(request, 'post/Likes.html',
                          {'likes': likes, 'message_obj': reply, 'message': letter, 'pages': pages})
        return render(request, 'post/Likes.html/', {'message': letter})


def who_disliked(request, letter, id_):
    if request.method == 'GET':
        if letter == 'Post':
            post = Post.objects.get(id=id_)
            dislikes = post.dislikes()
            page = request.GET.get('page', 1)
            paginator = Paginator(dislikes, 10)
            try:
                pages = paginator.page(page)
            except PageNotAnInteger:
                pages = paginator.page(1)
            except EmptyPage:
                pages = paginator.page(paginator.num_pages)

            return render(request, 'post/Dislikes.html',
                          {'dislikes': dislikes, 'message_obj': post, 'message': letter, 'pages': pages})
        elif letter == 'Comment':
            comment = Comment.objects.get(id=id_)
            dislikes = comment.dislikes()
            page = request.GET.get('page', 1)
            paginator = Paginator(dislikes, 10)
            try:
                pages = paginator.page(page)
            except PageNotAnInteger:
                pages = paginator.page(1)
            except EmptyPage:
                pages = paginator.page(paginator.num_pages)

            return render(request, 'post/Dislikes.html',
                          {'dislikes': dislikes, 'message_obj': comment, 'message': letter, 'pages': pages})
        elif letter == 'Reply':
            reply = Reply.objects.get(id=id_)
            dislikes = reply.dislikes()
            page = request.GET.get('page', 1)
            paginator = Paginator(dislikes, 10)
            try:
                pages = paginator.page(page)
            except PageNotAnInteger:
                pages = paginator.page(1)
            except EmptyPage:
                pages = paginator.page(paginator.num_pages)

            return render(request, 'post/Dislikes.html',
                          {'dislikes': dislikes, 'message_obj': reply, 'message': letter, 'pages': pages})
        return render(request, 'post/Dislikes.html', {'message': letter})


def return_page(a_letter, an_id):
    global my_id
    if a_letter == 'Post' or a_letter == 'Comment':
        if a_letter == 'Comment':
            my_id = int(Comment.objects.get(id=an_id).post.id)
        elif a_letter == 'Post':
            my_id = an_id
        return '/post/' + str(my_id)
    elif a_letter == 'Reply':
        comment_id = Reply.objects.get(id=an_id).comment.id
        post_id = Reply.objects.get(id=an_id).comment.post.id
        return '/post/' + str(post_id) + "/comment/" + str(comment_id)


def react(request):
    global m_letter
    if request.method == 'GET':
        letter = str(request.GET['message_type'])
        id_ = str(request.GET['message_id'])
        reaction = str(request.GET['reaction'])
        if letter == 'Post':
            m_letter = 'P'
        elif letter == 'Comment':
            m_letter = 'C'
        elif letter == 'Reply':
            m_letter = 'R'
        try:
            d_like = Reaction.objects.filter(reactor_id=request.user.id).filter(message_type=m_letter).get(
                message_id=id_)
        except Reaction.DoesNotExist:
            m_like = Reaction()
            m_like.reactor_id = request.user.id
            m_like.reaction = reaction
            m_like.message_id = id_
            m_like.message_type = m_letter
            m_like.save()
            return HttpResponse("success")
        else:
            d_like.reaction = reaction
            d_like.save()
            return HttpResponse("success")

    else:
        return HttpResponse("Request method is not a GET")


def get_page(page, item):
    paginator = Paginator(item, 10)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    return pages


def all_posts(request, tag):
    if tag == 't':
        posts = Post.objects.order_by('-date_posted').filter(for_cooperative__exact=False).all()
        return render(request, 'post/all_post.html', {'posts': posts})
    else:
        posts = Post.objects.order_by('-date_posted').filter(tag=tag, for_cooperative__exact=False).all()
        return render(request, 'post/all_post.html', {'posts': posts})


