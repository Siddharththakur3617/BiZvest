from django.urls import path
from . import views, admin_views

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
    path('offer/create/', views.create_offer, name='create_offer'),
    path('offer/cancel/<int:offer_id>/', views.cancel_offer, name='cancel_offer'),
    path('offer/accept/<int:offer_id>/', views.accept_offer, name='accept_offer'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    
    path('admin_panel/add_sector/', admin_views.add_sector_view, name='add_sector'),
    path('admin_panel/startups/', views.startup_list, name='startup_list'),
    path('admin_panel/investors/', views.investor_list, name='investor_list'),
    path('admin_panel/all_offers/', views.offer_list, name='offer_list'),
    path('admin_panel/all_deals/', admin_views.admin_all_deals, name='admin_all_deals'),
    path('admin_panel/dashboard/', admin_views.admin_dashboard_view, name='admin_dashboard'),
    path('admin_panel/profile/', admin_views.admin_profile_view, name='admin_profile'),
]