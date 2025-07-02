from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Startup, Investor, Deals, Offers, Sector, AppUser, Offers, Deals
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

def home(request):
    return render(request, 'home.html')

def startup_list(request):
    query = request.GET.get('q')
    sector = request.GET.get('sector')
    startups = Startup.objects.all()
    
    if query:
        startups = startups.filter(
            Q(startup_name__icontains=query) |
            Q(founder__icontains=query) |
            Q(descr__icontains=query)
        )
    if sector:
        startups = startups.filter(sector__sector_name=sector)
    
    sectors = Sector.objects.all()
    return render(request, 'startups.html', {'startups': startups, 'sectors': sectors})

def investor_list(request):
    query = request.GET.get('q')
    investors = Investor.objects.all()
    
    if query:
        investors = investors.filter(
            Q(founder__icontains=query) |
            Q(company_name__icontains=query) |
            Q(descr__icontains=query)
        )
    
    return render(request, 'investors.html', {'investors': investors})

def deal_list(request):
    deals = Deals.objects.select_related('startup', 'investor').all()
    return render(request, 'deals.html', {'deals': deals})

def offer_list(request):
    user_id = request.session.get('user_id')
    user = AppUser.objects.get(pk=user_id) if user_id else None

    offers = Offers.objects.select_related('startup').all()

    context = {
        'offers': offers,
        'is_startup': bool(user and user.startup),
        'is_investor': bool(user and user.investor),
        'user': user,
    }

    return render(request, 'offers.html', context)

def sector_list(request):
    sectors = Sector.objects.all()
    return render(request, 'sectors.html', {'sectors': sectors})

def login_view(request):
    error = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = AppUser.objects.get(username=username)
                if user.check_pass(password):
                    request.session['user_id'] = user.user_id
                    return redirect('home') 
                else:
                    error = "Invalid password"
            except AppUser.DoesNotExist:
                error = "User not found"
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'error': error})

def dashboard_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = AppUser.objects.get(pk=user_id)
    except AppUser.DoesNotExist:
        return HttpResponseForbidden("Invalid session.")

    context = {
        'user': user,
        'is_investor': user.investor is not None,
        'is_startup': user.startup is not None,
    }

    if user.investor:
        recent_deals = Deals.objects.filter(investor=user.investor).select_related('startup').order_by('-date_of_deal')[:]
        context['recent_deals'] = recent_deals

    elif user.startup:
        recent_offers = Offers.objects.filter(startup=user.startup).order_by('-offer_id')[:]
        context['recent_offers'] = recent_offers
    
    if user.startup:
        startup_msg = request.session.pop('startup_deal_message', None)
        if startup_msg:
            messages.success(request, startup_msg)

    return render(request, 'dashboard.html', context)

def profile_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = AppUser.objects.get(pk=user_id)
    except AppUser.DoesNotExist:
        return HttpResponseForbidden("Invalid session.")

    context = {
        'user': user,
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
        # GET requests
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

        # Create a new deal
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

        # Delete the offer
        offer.delete()

        # Message for investor
        messages.success(request, "Congratulations, Offer accepted and deal created !!")

        startup_user = AppUser.objects.filter(startup=deal.startup).first()
        if startup_user:
            request.session['startup_deal_message'] = f"🎉 Your offer has been accepted by {deal.investor.company_name}!"

    except Offers.DoesNotExist:
        messages.error(request, "Offer not found.")

    return redirect('dashboard')  