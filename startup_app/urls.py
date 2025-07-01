from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('startup/', views.startup_list, name='startup_list'),
    path('investor/', views.investor_list, name='investor_list'),
    path('deals/', views.deal_list, name='deal_list'),
    path('offers/', views.offer_list, name='offer_list'),
    path('sector/', views.sector_list, name='sector_list'),
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]