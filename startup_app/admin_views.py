from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Sector, Startup, Investor, Offers, Deals, AppUser
from .forms import SectorForm
from django.core.paginator import Paginator
from django.db.models import Q
import logging

logger = logging.getLogger('admin_actions')

def is_admin(request):
    return request.session.get('username') == 'admin'

def add_sector_view(request):
    if not request.session.get('is_admin'):
        return HttpResponseForbidden("Only admin can access this.")

    if request.method == 'POST':
        form = SectorForm(request.POST)
        if form.is_valid():
            sector_name = form.cleaned_data['sector_name']
            if Sector.objects.filter(sector_name=sector_name).exists():
                messages.error(request, f"Sector '{sector_name}' already exists.")
                logger.warning(f"Admin attempted to add duplicate sector '{sector_name}'")
            else:
                form.save()
                messages.success(request, f"Sector '{sector_name}' added successfully.")
                logger.info(f"Admin added sector '{sector_name}'")
                return redirect('add_sector')
        else:
            messages.error(request, "Invalid input. Please check the form.")
    else:
        form = SectorForm()

    return render(request, 'admin_add_sector.html', {'form': form})

def admin_all_deals(request):
    if not request.session.get('is_admin'):
        return HttpResponseForbidden("Only admin can access this.")

    deals = Deals.objects.select_related('startup', 'investor').all()
    query = request.GET.get('q')
    if query:
        deals = deals.filter(
            Q(startup_startup_name_icontains=query) |
            Q(investor_company_name_icontains=query)
        )

    paginator = Paginator(deals, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_all_deals.html', {'page_obj': page_obj, 'query': query})

def admin_dashboard_view(request):
    if not request.session.get('is_admin'):
        return HttpResponseForbidden("Only admin can access this.")

    user = type('AdminUser', (), {'username': 'admin'})()
    context = {
        'user': user,
        'is_admin': True,
        'is_startup': False,
        'is_investor': False,
        'deal_count': Deals.objects.count(),
        'offer_count': Offers.objects.count(),
        'app_users': AppUser.objects.all(),
    }
    return render(request, 'dashboard.html', context)

def admin_profile_view(request):
    if not request.session.get('is_admin'):
        return HttpResponseForbidden("Only admin can access this.")

    user = type('AdminUser', (), {'username': 'admin'})()
    context = {
        'user': user,
        'is_admin': True,
        'is_startup': False,
        'is_investor': False,
    }
    return render(request, 'profile.html', context)