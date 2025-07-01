from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('startup_app_startup/', views.startup_list, name='startup_list'),
    path('startup_app_investor/', views.investor_list, name='investor_list'),
    path('startup_app_deals/', views.deal_list, name='deal_list'),
    path('startup_app_offers/', views.offer_list, name='offer_list'),
    path('startup_app_sector/', views.sector_list, name='sector_list'),
]