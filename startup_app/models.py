# from django.db import models
# from django.core.exceptions import ValidationError
# # Create your models here.

# class Sector(models.Model):
#     sector_name = models.CharField(max_length=100, primary_key=True)

#     def __str__(self):
#         return self.sector_name
    
# class Startup(models.Model):
#     startup_id = models.AutoField(primary_key=True)
#     startup_name = models.CharField(max_length=100)
#     descr = models.TextField()
#     founder = models.CharField(max_length=100)
#     valuation = models.PositiveIntegerField()
#     last_year_profit = models.IntegerField(null=True, blank=True)
#     burn_rate = models.FloatField(null=True, blank=True)
#     contact_no = models.CharField(max_length=13)
#     email_id = models.EmailField(max_length=50)
#     sector = models.ForeignKey(Sector, to_field='sector_name', on_delete=models.CASCADE)

#     class Meta:
#         db_table = "startup"  # 👈 Force Django to use your existing MySQL table

#     def __str__(self):
#         return self.startup_name

    
# class Investor(models.Model):
#     investor_id = models.AutoField(primary_key=True)
#     founder = models.CharField(max_length=100)
#     company_name = models.CharField(max_length=100)
#     descr = models.TextField(null=True, blank=True)

#     # Ensuring net_worth > 0
#     net_worth = models.PositiveIntegerField()
    
#     contact_no = models.CharField(max_length=13)
#     email = models.EmailField(max_length=100)  # Use EmailField for validation

#     def __str__(self):
#         return self.company_name
    
# class Choices(models.Model):
#     investor = models.ForeignKey('Investor', on_delete=models.CASCADE)
#     sector = models.ForeignKey('Sector', to_field='sector_name', on_delete=models.CASCADE)
    
#     # Interest must be between 0 and 100
#     interest = models.FloatField()

#     class Meta:
#         unique_together = ('investor', 'sector')

#     def __str__(self):
#         return f"{self.investor.company_name} → {self.sector.sector_name} ({self.interest}%)"

# class Deals(models.Model):
#     deal_id = models.AutoField(primary_key=True)
    
#     startup = models.ForeignKey('Startup', on_delete=models.CASCADE)
#     investor = models.ForeignKey('Investor', on_delete=models.CASCADE)

#     # Prefer DateField for dates — cleaner and safer than CharField
#     date_of_deal = models.DateField()

#     amount_invested = models.PositiveIntegerField(default=0)
#     loan_given = models.PositiveIntegerField(default=0)
#     loan_time = models.PositiveIntegerField(default=0)  # time in months or years?
#     loan_rate = models.FloatField(default=0.0)
#     equity = models.FloatField(default=0.0)

#     def __str__(self):
#         return f"Deal #{self.deal_id} between {self.investor.company_name} and {self.startup.startup_name}"
    
# from django.db import models

# class Offers(models.Model):
#     offer_id = models.AutoField(primary_key=True)
#     startup = models.ForeignKey('Startup', on_delete=models.CASCADE)

#     investment_asked = models.PositiveIntegerField(default=0)
#     equity_offered = models.FloatField(default=0.0)
#     loan_req = models.PositiveIntegerField(default=0)
#     loan_rate = models.FloatField(default=0.0)
#     loan_time = models.PositiveIntegerField(default=12)

#     def __str__(self):
#         return f"Offer #{self.offer_id} by {self.startup.startup_name}"
    
# class AppUser(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     investor = models.ForeignKey('Investor', on_delete=models.CASCADE, null=True, blank=True)
#     startup = models.ForeignKey('Startup', on_delete=models.CASCADE, null=True, blank=True)

#     class Meta:
#         constraints = [
#             models.CheckConstraint(
#                 check=(
#                     models.Q(investor__isnull=False) | 
#                     models.Q(startup__isnull=False)
#                 ),
#                 name='investor_or_startup_not_null'
#             )
#         ]

#     def clean(self):
#         if not self.investor and not self.startup:
#             raise ValidationError("At least one of investor or startup must be set.")

#     def __str__(self):
#         if self.investor:
#             return f"User (Investor: {self.investor.company_name})"
#         if self.startup:
#             return f"User (Startup: {self.startup.startup_name})"
#         return f"User #{self.user_id}"

from django.db import models
from django.core.exceptions import ValidationError

class Sector(models.Model):
    sector_name = models.CharField(max_length=100, primary_key=True)

    class Meta:
        db_table = "Sector"  # Match class name exactly

    def __str__(self):
        return self.sector_name


class Startup(models.Model):
    startup_id = models.AutoField(primary_key=True)
    startup_name = models.CharField(max_length=100)
    descr = models.TextField()
    founder = models.CharField(max_length=100)
    valuation = models.PositiveIntegerField()
    last_year_profit = models.IntegerField(null=True, blank=True)
    burn_rate = models.FloatField(null=True, blank=True)
    contact_no = models.CharField(max_length=13)
    email_id = models.EmailField(max_length=50)

    sector = models.ForeignKey(
        'Sector',
        to_field='sector_name',
        db_column='sector',  # 👈 matches your MySQL table
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "Startup"

    def __str__(self):
        return self.startup_name


class Investor(models.Model):
    investor_id = models.AutoField(primary_key=True)
    founder = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    descr = models.TextField(null=True, blank=True)
    net_worth = models.PositiveIntegerField()
    contact_no = models.CharField(max_length=13)
    email = models.EmailField(max_length=100)

    class Meta:
        db_table = "Investor"

    def __str__(self):
        return self.company_name


class Choices(models.Model):
    investor = models.ForeignKey('Investor', on_delete=models.CASCADE)
    sector = models.ForeignKey(
        'Sector',
        to_field='sector_name',
        db_column='sector_name',
        on_delete=models.CASCADE
    )
    interest = models.FloatField()

    class Meta:
        db_table = "Choices"
        unique_together = ('investor', 'sector')

    def __str__(self):
        return f"{self.investor.company_name} → {self.sector.sector_name} ({self.interest}%)"


class Deals(models.Model):
    deal_id = models.AutoField(primary_key=True)
    startup = models.ForeignKey('Startup', on_delete=models.CASCADE)
    investor = models.ForeignKey('Investor', on_delete=models.CASCADE)
    date_of_deal = models.DateField()
    amount_invested = models.PositiveIntegerField(default=0)
    loan_given = models.PositiveIntegerField(default=0)
    loan_time = models.PositiveIntegerField(default=0)
    loan_rate = models.FloatField(default=0.0)
    equity = models.FloatField(default=0.0)

    class Meta:
        db_table = "Deals"

    def __str__(self):
        return f"Deal #{self.deal_id} between {self.investor.company_name} and {self.startup.startup_name}"


class Offers(models.Model):
    offer_id = models.AutoField(primary_key=True)
    startup = models.ForeignKey('Startup', on_delete=models.CASCADE)
    investment_asked = models.PositiveIntegerField(default=0)
    equity_offered = models.FloatField(default=0.0)
    loan_req = models.PositiveIntegerField(default=0)
    loan_rate = models.FloatField(default=0.0)
    loan_time = models.PositiveIntegerField(default=12)

    class Meta:
        db_table = "Offers"

    def __str__(self):
        return f"Offer #{self.offer_id} by {self.startup.startup_name}"


class AppUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    investor = models.ForeignKey('Investor', on_delete=models.CASCADE, null=True, blank=True)
    startup = models.ForeignKey('Startup', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "AppUser"
        constraints = [
            models.CheckConstraint(
                check=(models.Q(investor__isnull=False) | models.Q(startup__isnull=False)),
                name='investor_or_startup_not_null'
            )
        ]

    def clean(self):
        if not self.investor and not self.startup:
            raise ValidationError("At least one of investor or startup must be set.")

    def __str__(self):
        if self.investor:
            return f"User (Investor: {self.investor.company_name})"
        if self.startup:
            return f"User (Startup: {self.startup.startup_name})"
        return f"User #{self.user_id}"