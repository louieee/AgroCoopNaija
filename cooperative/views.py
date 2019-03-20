from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group, User
from cooperative.models import Cooperative, Member
from post.models import Post
import django.utils.timezone


# Create your views here.
def create_coop(request):
    if request.method == 'POST':
        name = request.POST.get('name', False)
        location = request.POST.get('location', False)
        image = request.FILES.get('image', False)
        website = request.POST.get('website', False)
        email = request.POST.get('email', False)
        desc = request.POST.get('desc', False)
        if name and location and image and website and email and desc:
            if Cooperative.objects.get(name=name).DoesNotExist:
                if Cooperative.objects.get(email=email).DoesNotExist:
                    coop = Cooperative()
                    coop.name = name
                    coop.location = location
                    coop.image = image
                    coop.website = website
                    coop.about = desc
                    coop.email = email
                    coop.save()
                    return redirect('home', {'message': 'Your Cooperative has been created', 'status': 'success'})
                else:
                    return render(request, '../cooperative/templates/cooperative/create_coop.html',
                                  {'message': 'A cooperative already has this email address',
                                   'status': 'danger'})
            else:
                return render(request, '../cooperative/templates/cooperative/create_coop.html',
                              {'message': 'A cooperative with this name already exists',
                               'status': 'danger'})
        else:
            return render(request, '../cooperative/templates/cooperative/create_coop.html',
                          {'message': 'All fields must be filled',
                           'status': 'danger'})
    return render(request, '../cooperative/templates/cooperative/create_coop.html')


def be_coop_member(request, id_):
    if request.method == 'POST':
        dob = request.POST.get('dob', False)
        coop = Cooperative.objects.get(id=id_)
        if dob:
            if Member.objects.get(user_email=request.user.email, user_username=request.user.username, cooperative_id=id)\
                    .DoesNotExist:
                m_member = Member()
                m_member.user_id = request.user.id
                m_member.date_of_birth = dob
                m_member.cooperative_id = coop.id
                m_member.time_of_request = django.utils.timezone.datetime.now()
                m_member.save()
                return redirect('home',
                                {'message': 'You have successfully declared your interest ', 'status': 'success'})
            else:
                return render(request, '../cooperative/templates/cooperative/all_cooperatives.html',
                              {'message': 'You are already a member of this '
                                          'cooperative ', 'status': 'danger'})
        else:
            return render(request, '../cooperative/templates/cooperative/all_cooperatives.html',
                          {'message': 'All fields must be filled',
                           'status': 'danger'})

    return render(request, '../partner/templates/partner/be_partner.html')


def all_cooperatives(request):
    all_coop = Cooperative().objects.all()
    return render(request, '../cooperative/templates/cooperative/all_cooperatives.html', {'cooperative': all_coop})


def dashboard_coop(request, username):
    member = get_object_or_404(Member, username=username)
    name = member.cooperative.name
    posts = Post.objects.order_by('date_posted').get(coop_name=name).objects.all()
    members = Member.objects.order_by('time_of_request').get(cooperative__name=name,
                                                             date_of_admission__isnull=True).objects.all()
    return render(request, '../cooperative/templates/cooperative/Dashboard-coop.html',
                  {'member': member, 'posts': posts, 'members': members})
