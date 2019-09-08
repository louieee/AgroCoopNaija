from django.shortcuts import render
from core.models import User
from partner.models import Partner
from my_methods import Tag, get_pagination, degree_to_title, degrees
from core.decorators import active_member_required
from django.contrib.auth.decorators import login_required


# Create your views here.
# This view takes all partners from the database and displays it onto the all partners page
def all_partners(request, page):
    partners = Partner.objects.all().order_by('user_id')
    partners_list = get_pagination(page, partners)
    return render(request, 'partner/all_partners.html', {'partners': partners_list})


# This view enables a user to make a request to be a partner. It adds a new partner to the database
@login_required(login_url='home')
def be_partner(request):
    tags = Tag.tags
    all_degrees = degrees
    if request.method == 'POST':
        corp_name = request.POST.get('corp_name', False)
        bio = request.POST.get('bio', False)
        degree = request.POST.get('degree', False)
        spec = str(request.POST.get('spec', False))
        position = str(request.POST.get('position', False))
        web = request.POST.get('web', False)

        def add_partner():
            m_partner = Partner()
            m_partner.user = user
            m_partner.website = web
            m_partner.biography = bio
            title = degree_to_title(str(degree))
            if title != 'None':
                m_partner.user.title = title + m_partner.user.title
            m_partner.position = position
            m_partner.institution = corp_name
            m_partner.specialization = spec
            m_partner.save()

        if corp_name and bio and spec and web and position:
            user = User.objects.get(id=request.user.id)
            try:
                Partner.objects.get(user_id=user.id)
                return render(request, 'partner/be_partner.html',
                              {'message': 'You are already a partner',
                               'status': 'danger', 'tags': tags, 'degrees': all_degrees})
            except Partner.DoesNotExist:
                try:
                    d_partner = Partner.objects.get(institution=corp_name)
                    if d_partner.user_detail().first_name == user.first_name and d_partner.user_detail().last_name == user.last_name:
                        return render(request, 'partner/be_partner.html',
                                      {'message': 'A partner with this name  already exists',
                                       'status': 'danger', 'tags': tags, 'degrees': all_degrees})
                    else:
                        add_partner()
                        return render(request, 'core/home.html',
                                      {'message': 'You have successfully become a partner', 'status': 'success'})
                except Partner.DoesNotExist:
                    add_partner()
                    return render(request, 'core/home.html',
                                  {'message': 'You have successfully become a partner', 'status': 'success'})

        else:
            return render(request, 'partner/be_partner.html',
                          {'message': 'All fields must be filled',
                           'status': 'danger', 'tags': tags})
    return render(request, 'partner/be_partner.html', {'tags': tags, 'degrees': all_degrees})


# This view gets all the information of a partner from database and displays it
@active_member_required
def partner_detail(request, id_):
    partner = Partner.objects.get(user_id=id_)
    return render(request, 'partner/partner_detail.html', {'partner': partner})
