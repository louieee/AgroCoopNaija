from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import auth
from partner.models import Partner


# Create your views here.
def all_partners(request):
    partners = Partner().objects.all()
    return render(request, '../partner/templates/partner/all_partners.html', {'partners': partners})


def be_partner(request):
    if request.method == 'POST':
        corp_name = request.POST.get('corp_name', False)
        bio = request.POST.get('bio', False)
        inst = request.POST.get('inst', False)
        web = request.POST.get('web', False)
        if corp_name and bio and inst and web:
            user = auth.get_user_model()
            partner = Partner.objects.get(user=user)
            if partner.DoesNotExist:
                d_partner = Partner.objects.get(corporate_name=corp_name)
                if d_partner.DoesNotExist:
                    m_partner = Partner()
                    m_partner.user = user
                    m_partner.website = web
                    m_partner.biography = bio
                    m_partner.corporate_name = corp_name
                    m_partner.institution = inst
                    m_partner.save()
                    user.is_partner = True
                    user.save()
                    return redirect('home', {'message': 'You have successfully become a partner', 'status': 'success'})
                else:
                    return render(request, '../partner/templates/partner/be_partner.html',
                                  {'message': 'A partner already has this corporate name',
                                   'status': 'danger'})
            else:
                return render(request, '../partner/templates/partner/be_partner.html',
                              {'message': 'You are already a partner',
                               'status': 'danger'})
        else:
            return render(request, '../partner/templates/partner/be_partner.html',
                          {'message': 'All fields must be filled',
                           'status': 'danger'})

    return render(request, '../partner/templates/partner/be_partner.html')


def partner_detail(request, username):
    partner = get_object_or_404(Partner, username=username)
    return render(request, '../partner/templates/partner/partner_detail.html', {'partner': partner})


def dashboard_partner(request, username):
    partner = get_object_or_404(Partner, username=username)
    posts = get_list_or_404(Post, author=partner.user)
    return render(request, '../partner/templates/partner/Dashboard-partner.html', {'partner': partner, 'posts': posts})
