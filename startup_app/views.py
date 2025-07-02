from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Startup, Investor, Deals, Offers, Sector, AppUser, Choices
from django.http import HttpResponseForbidden
from django.contrib import messages
from .forms import (
    LoginForm,
    UserTypeForm,
    InvestorRegistrationForm,
    StartupRegistrationForm,
    OfferCreationForm
)
from datetime import date
import logging

logger = logging.getLogger('admin_login')

def home(request):
    return render(request, 'home.html')

def startup_list(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    if user_id:
        startups = Startup.objects.all()
    else:
        startups = Startup.objects.none()

    sectors = Sector.objects.all()
    return render(request, 'startups.html', {'startups': startups, 'sectors': sectors})

def investor_list(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    if user_id:
        investors = Investor.objects.all()
    else:
        investors = Investor.objects.none()

    query = request.GET.get('q')
    if query:
        investors = investors.filter(
            Q(founder__icontains=query) |
            Q(company_name__icontains=query) |
            Q(descr__icontains=query)
        )

    return render(request, 'investors.html', {'investors': investors})

def deal_list(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    if request.session.get('username') == "admin":
        deals = Deals.objects.select_related('startup', 'investor').all() 
    else:     
        user = AppUser.objects.get(pk=user_id)
        if user.investor:
           deals = Deals.objects.filter(investor=user.investor).select_related('startup')
        elif user.startup:
           deals = Deals.objects.filter(startup=user.startup).select_related('investor')
        else:
           deals = Deals.objects.none()
    return render(request, 'deals.html', {'deals': deals})

def offer_list(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    if user_id or request.session.get('is_admin'):
        offers = Offers.objects.select_related('startup').all()
    else:
        offers = Offers.objects.none()

    return render(request, 'offers.html', {'offers': offers})

def sector_list(request):
    user_id = request.session.get('user_id')
    if not user_id and not request.session.get('is_admin'):
        return redirect('login')
    selected_sector = request.GET.get('sector', 'all')
    selected_type = request.GET.get('type', 'all')

    sectors = Sector.objects.all()
    sector_data = []

    for sector in sectors:
        data = {'sector': sector, 'startups': [], 'investors': []}
        if selected_type in ['all', 'startup']:
            startups = Startup.objects.filter(sector=sector)
            if selected_sector != 'all' and sector.sector_name != selected_sector:
                startups = startups.none()
            data['startups'] = startups

        if selected_type in ['all', 'investor']:
            investor_ids = Choices.objects.filter(sector=sector).values_list('investor', flat=True)
            investors = Investor.objects.filter(investor_id__in=investor_ids)
            if selected_sector != 'all' and sector.sector_name != selected_sector:
                investors = investors.none()
            data['investors'] = investors

        if selected_sector == 'all' or data['startups'] or data['investors']:
            sector_data.append(data)

    context = {
        'sectors': sectors,
        'sector_data': sector_data,
        'selected_sector': selected_sector,
        'selected_type': selected_type,
    }

    return render(request, 'sectors.html', context)

def delete_user(request, user_id):
    logger = logging.getLogger('admin_actions')
    if not request.session.get('is_admin'):
        return HttpResponseForbidden("Only admin can delete users.")

    if request.method == 'POST':
        try:
            user_to_delete = AppUser.objects.get(pk=user_id)
            if user_to_delete.username == 'admin':
                messages.error(request, "Cannot delete the admin account.")
                logger.warning("Attempt to delete admin account blocked")
            else:
                username = user_to_delete.username
                user_to_delete.delete()
                messages.success(request, f"User '{username}' deleted successfully.")
                logger.info(f"Admin deleted user '{username}' (ID: {user_id})")
        except AppUser.DoesNotExist:
            messages.error(request, "User not found.")
            logger.warning(f"Admin attempted to delete non-existent user ID {user_id}")
        return redirect('dashboard')
    
    try:
        user_to_delete = AppUser.objects.get(pk=user_id)
        return render(request, 'confirm_delete_user.html', {'user_to_delete': user_to_delete})
    except AppUser.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('dashboard')

def login_view(request):
    error = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if username == 'admin':
                if password == 'admin123':
                    request.session['username'] = 'admin'
                    request.session['user_id'] = 1001
                    request.session['is_admin'] = True
                    logger.info("Admin logged in successfully")
                    return redirect('dashboard')
                else:
                    error = "Invalid password for admin"
                    logger.warning(f"Failed admin login attempt with password: {password}")
            else:
                try:
                    user = AppUser.objects.get(username=username)
                    if user.check_pass(password):
                        request.session['user_id'] = user.user_id
                        request.session['is_admin'] = False
                        request.session['username'] = username
                        logger.info(f"User {username} logged in successfully")
                        return redirect('dashboard')
                    else:
                        error = "Invalid password"
                        logger.warning(f"Failed login attempt for user substituting user {username}")
                except AppUser.DoesNotExist:
                    error = "User not found"
                    logger.warning(f"Login attempt for non-existent user {username}")
        else:
            error = "Invalid form input"
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'error': error})

def dashboard_view(request):
    if request.session.get('is_admin'):
        user = type('AdminUser', (), {'username': 'admin'})()
        context = {
            'user': user,
            'is_admin': True,
            'is_startup': False,
            'is_investor': False,
        }
        return render(request, 'dashboard.html', context)

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = AppUser.objects.get(pk=user_id)
    except AppUser.DoesNotExist:
        return HttpResponseForbidden("Invalid session.")

    context = {
        'user': user,
        'is_admin': False,
        'is_investor': user.investor is not None,
        'is_startup': user.startup is not None,
    }

    if user.investor:
        context['recent_deals'] = Deals.objects.filter(investor=user.investor).select_related('startup')[:5]
    elif user.startup:
        context['recent_offers'] = Offers.objects.filter(startup=user.startup)[:5]

    return render(request, 'dashboard.html', context)

def profile_view(request):
    user_id = request.session.get('user_id')

    if user_id is None:
        return redirect('login')

    if request.session.get('is_admin'):
        user = type('AdminUser', (), {'username': 'admin'})()
        context = {
            'user': user,
            'is_admin': True,
            'is_startup': False,
            'is_investor': False,
        }
        return render(request, 'profile.html', context)

    try:
        user = AppUser.objects.get(pk=user_id)
    except AppUser.DoesNotExist:
        return HttpResponseForbidden("Invalid session.")

    context = {
        'user': user,
        'is_admin': False,
        'is_investor': user.investor is not None,
        'is_startup': user.startup is not None,
    }

    return render(request, 'profile.html', context)

def logout_view(request):
    request.session.flush()
    return redirect('login')

def register_view(request):
    step = request.GET.get('step', 'type') 

    if request.method == 'POST':
        if 'user_type' in request.POST:
            form = UserTypeForm(request.POST)
            if form.is_valid():
                user_type = form.cleaned_data['user_type']
                return redirect(f"{request.path}?step={user_type}")
        elif request.GET.get('step') == 'investor':
            form = InvestorRegistrationForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                if AppUser.objects.filter(username=data['username']).exists():
                    form.add_error('username', 'Username already taken')
                else:
                    investor = Investor.objects.create(
                        founder=data['founder'],
                        company_name=data['company_name'],
                        net_worth=data['net_worth'],
                        contact_no=data['contact_no'],
                        email=data['email'],
                        descr=data['descr']
                    )
                    user = AppUser(username=data['username'], investor=investor)
                    user.set_password(data['password'])
                    user.save()
                    return redirect('login')
        elif request.GET.get('step') == 'startup':
            form = StartupRegistrationForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                if AppUser.objects.filter(username=data['username']).exists():
                    form.add_error('username', 'Username already taken')
                else:
                    startup = Startup.objects.create(
                        startup_name=data['startup_name'],
                        founder=data['founder'],
                        valuation=data['valuation'],
                        contact_no=data['contact_no'],
                        email_id=data['email_id'],
                        sector=data['sector'],
                        descr=data['descr']
                    )
                    user = AppUser(username=data['username'], startup=startup)
                    user.set_password(data['password'])
                    user.save()
                    return redirect('login')
    else:
        if step == 'investor':
            form = InvestorRegistrationForm()
        elif step == 'startup':
            form = StartupRegistrationForm()
        else:
            form = UserTypeForm()

    return render(request, 'register.html', {'form': form, 'step': step})

def create_offer(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = AppUser.objects.get(pk=user_id)
    if not user.startup:
        return HttpResponseForbidden("Only startups can create offers.")

    if request.method == 'POST':
        form = OfferCreationForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.startup = user.startup
            offer.save()
            messages.success(request, "Offer created successfully.")
            return redirect('dashboard')
    else:
        form = OfferCreationForm()

    return render(request, 'create_offer.html', {'form': form})

def cancel_offer(request, offer_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = AppUser.objects.get(pk=user_id)
    if not user.startup:
        return HttpResponseForbidden("Only startups can cancel offers.")

    try:
        offer = Offers.objects.get(pk=offer_id, startup=user.startup)
        offer.delete()
        messages.success(request, "Offer cancelled.")
    except Offers.DoesNotExist:
        messages.error(request, "Offer not found or access denied.")

    return redirect('dashboard')

def accept_offer(request, offer_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = AppUser.objects.get(pk=user_id)
    if not user.investor:
        return HttpResponseForbidden("Only investors can accept offers.")

    try:
        offer = Offers.objects.get(pk=offer_id)
        deal = Deals.objects.create(
            startup=offer.startup,
            investor=user.investor,
            date_of_deal=date.today(),
            amount_invested=offer.investment_asked,
            loan_given=offer.loan_req,
            loan_time=offer.loan_time,
            loan_rate=offer.loan_rate,
            equity=offer.equity_offered
        )
        offer.delete()
        messages.success(request, "Congratulations, Offer accepted and deal created !!")
        startup_user = AppUser.objects.filter(startup=deal.startup).first()
        if startup_user:
            request.session['startup_deal_message'] = f"🎉 Your offer has been accepted by {deal.investor.company_name}!"
    except Offers.DoesNotExist:
        messages.error(request, "Offer not found.")

    return redirect('dashboard')
