from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from cooperative.models import Cooperative, Member
from product.models import Order
from wallet.models import Wallet
from post.models import Post
import django.utils.timezone
from django.contrib.auth.hashers import MD5PasswordHasher as Hash


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
                if Cooperative.objects.get(email=email).DoesNotExist and Wallet.objects.get(
                        email=email).DoesNotExist:
                    coop = Cooperative()
                    coop.name = name
                    coop.location = location
                    coop.image = image
                    coop.website = website
                    coop.about = desc
                    coop.email = email
                    m_wallet = Wallet()
                    m_wallet.email = email
                    m_wallet.acct_name = name
                    m_wallet.acct_number = Hash().salt()
                    m_wallet.save()
                    coop.wallet = m_wallet
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


def be_coop_member(request):
    if request.method == 'POST':
        corp_name = str(request.POST.get('corp_name', False))
        dob = request.POST.get('dob', False)
        if corp_name and dob:
            user = auth.get_user_model()
            mem = Member.objects.get(user=user, cooperative__name=corp_name)
            if mem.DoesNotExist:
                coop = Cooperative.objects.get(name=corp_name)
                m_member = Member()
                m_member.email = user.email
                m_member.date_of_birth = dob
                m_member.cooperative = coop
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
    orders = Order().objects.get(products__coop=member.cooperative).objects.all()
    posts = Post.objects.order_by('date_posted').get(coop_name=name).objects.all()
    members = Member.objects.order_by('time_of_request').get(cooperative__name=name,
                                                             date_of_admission__isnull=True).objects.all()
    return render(request, '../cooperative/templates/cooperative/Dashboard-coop.html',
                  {'member': member, 'posts': posts, 'orders': orders,
                   'members': members})
