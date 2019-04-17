from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import auth
from partner.models import Partner
from post.models import Post
from Lists import Tag
import re


# Create your views here.
def all_partners(request):
    partners = Partner.objects.all()
    return render(request, 'partner/all_partners.html', {'partners': partners})


def be_partner(request):
    tags = Tag.tags
    if request.method == 'POST':
        corp_name = request.POST.get('corp_name', False)
        bio = request.POST.get('bio', False)
        spec = list(request.POST.getlist('spec', False))
        web = request.POST.get('web', False)
        if corp_name and bio and spec and web:
            user = request.user
            partner = Partner.objects.get(user_id=user.id)
            if partner.DoesNotExist:
                d_partner = Partner.objects.get(corporate_name=corp_name)
                if d_partner.DoesNotExist:
                    m_partner = Partner()
                    m_partner.user = user
                    m_partner.website = web
                    m_partner.image = request.user.image
                    m_partner.biography = bio
                    m_partner.corporate_name = corp_name
                    real_spec = ''
                    for val in spec:
                        real_spec = val+';'
                    m_partner.specialization = real_spec
                    m_partner.save()
                    user.save()
                    return redirect('home', {'message': 'You have successfully become a partner', 'status': 'success'})
                else:
                    return render(request, 'partner/be_partner.html',
                                  {'message': 'A partner already has this corporate name',
                                   'status': 'danger', 'tags': tags})
            else:
                return render(request, 'partner/be_partner.html',
                              {'message': 'You are already a partner',
                               'status': 'danger', 'tags': tags})
        else:
            return render(request, 'partner/be_partner.html',
                          {'message': 'All fields must be filled',
                           'status': 'danger', 'tags': tags})
    return render(request, 'partner/be_partner.html', {'tags': tags})


def partner_detail(request, id_):
    partner = get_object_or_404(Partner, pk=id_)
    partners = Partner.objects.all().order_by('-id')[:10][-1]
    my_tags = partner.specialization
    return render(request, 'partner/partner_detail.html', {'partner': partner, 'tags': my_tags, 'partners': partners})


