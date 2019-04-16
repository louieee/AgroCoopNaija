from django.shortcuts import render, redirect, get_object_or_404
import django.utils.timezone as b
from cooperative.models import Cooperative, Member, MembershipRequest
from core.models import Tag, Bank


# Create your views here.
def create_coop(request):
    tags = Tag.tags
    banks = Bank.bank
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
                    return render(request, 'cooperative/create_coop.html',
                                  {'message': 'A cooperative already has this email address',
                                   'status': 'danger', 'tags': tags, 'banks': banks})
            else:
                return render(request, 'cooperative/create_coop.html',
                              {'message': 'A cooperative with this name already exists',
                               'status': 'danger', 'tags': tags, 'banks': banks})
        else:
            return render(request, 'cooperative/create_coop.html',
                          {'message': 'All fields must be filled',
                           'status': 'danger', 'tags': tags, 'banks': banks})
    return render(request, 'cooperative/create_coop.html', {'tags': tags, 'banks': banks})


def be_coop_member(request):
    if request.method == 'POST':
        id_ = request.POST.get('id_', False)
        coop = Cooperative(id=id_)
        if request.user.is_authenticated:
            request_ = MembershipRequest()
            request_.sender_id = request.user.id
            request_.time_of_request = b.now()
            request_.name = request.user.first_name + " " + request.user.last_name
            request_.cooperative_id = coop.id
            request_.email = request.user.email
            request_.save()
            return redirect('all_cooperatives',
                            {'message': 'You have Successfully sent a Membership Request to ' + coop.name,
                             'status': 'success'})

    return render(request, 'cooperative/all_cooperatives.html')


def all_cooperatives(request):
    all_coop = Cooperative.objects.all()
    return render(request, 'cooperative/all_cooperatives.html', {'cooperative': all_coop})



def coop_detail(request, _id):
    coop = get_object_or_404(Cooperative, id=_id)
    rel_coop = Cooperative.objects.all().filter(Area_of_Specialization=coop.Area_of_Specialization)
    return render(request, 'cooperative/coop_detail.html', {'coop': coop, 'rel': rel_coop})
