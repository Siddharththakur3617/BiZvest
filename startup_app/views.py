from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Startup, Investor, Deals, Offers, Sector
from .forms import LoginForm
from .models import AppUser
# Create your views here.

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
    offers = Offers.objects.select_related('startup').all()
    return render(request, 'offers.html', {'offers': offers})

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
                    return redirect('home')  # redirect to home after login
                else:
                    error = "Invalid password"
            except AppUser.DoesNotExist:
                error = "User not found"
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'error': error})