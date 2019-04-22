from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from core.models import User
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
            user = User.objects.get(id=request.user.id)
            try:
                partner = Partner.objects.get(user_id=user.id)
            except Partner.DoesNotExist:
                try:
                    d_partner = Partner.objects.get(corporate_name=corp_name)
                except Partner.DoesNotExist:
                    m_partner = Partner()
                    m_partner.user = user
                    m_partner.website = web
                    m_partner.biography = bio
                    m_partner.corporate_name = corp_name
                    m_partner.specialization = spec
                    m_partner.save()
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
    partner = Partner.objects.get(user_id=id_)
    return render(request, 'partner/partner_detail.html', {'partner': partner})


