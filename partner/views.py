from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from core.models import User
from partner.models import Partner
from my_methods import Tag, get_pagination


# Create your views here.
def all_partners(request, page):
    partners = Partner.objects.all().order_by('user_id')
    partners_list = get_pagination(page, partners)
    return render(request, 'partner/all_partners.html', {'partners': partners_list})


def be_partner(request):
    tags = Tag.tags
    if request.method == 'POST':
        corp_name = request.POST.get('corp_name', False)
        bio = request.POST.get('bio', False)
        spec = str(request.POST.get('spec', False))
        position = str(request.POST.get('position', False))
        web = request.POST.get('web', False)
        if corp_name and bio and spec and web and position:
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
                    m_partner.position = position
                    m_partner.institution = corp_name
                    m_partner.specialization = spec
                    m_partner.save()
                    return render(request, 'core/home.html', {'message': 'You have successfully become a partner', 'status': 'success'})
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


