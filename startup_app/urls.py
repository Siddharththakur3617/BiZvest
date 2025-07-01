from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('startup/', views.startup_list, name='startup_list'),
    path('investor/', views.investor_list, name='investor_list'),
    path('deals/', views.deal_list, name='deal_list'),
    path('offers/', views.offer_list, name='offer_list'),
    path('sector/', views.sector_list, name='sector_list'),
]

urlpatterns += [
    path('', views.login_view, name='login'),
]