from django.contrib import admin
from .models import Startup, Investor, Deals, Offers, Sector, Choices, AppUser

admin.site.register(Startup)
admin.site.register(Investor)
admin.site.register(Deals)
admin.site.register(Offers)
admin.site.register(Sector)
admin.site.register(Choices)
admin.site.register(AppUser)