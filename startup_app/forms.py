from django import forms
from .models import Startup, Investor, Sector, Offers

class OfferCreationForm(forms.ModelForm):
    class Meta:
        model = Offers
        fields = ['investment_asked', 'equity_offered', 'loan_req', 'loan_rate', 'loan_time']

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class UserTypeForm(forms.Form):
    user_type = forms.ChoiceField(
        choices=[('investor', 'Investor'), ('startup', 'Startup')],
        widget=forms.RadioSelect,
        label="Register as"
    )

class InvestorRegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    founder = forms.CharField(max_length=100)
    company_name = forms.CharField(max_length=100)
    net_worth = forms.IntegerField()
    contact_no = forms.CharField(max_length=13)
    email = forms.EmailField()
    descr = forms.CharField(widget=forms.Textarea, required=False)

class StartupRegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    founder = forms.CharField(max_length=100)
    startup_name = forms.CharField(max_length=100)
    valuation = forms.IntegerField()
    contact_no = forms.CharField(max_length=13)
    email_id = forms.EmailField(label="Email")
    sector = forms.ModelChoiceField(queryset=Sector.objects.all(), empty_label="Select Sector")
    descr = forms.CharField(widget=forms.Textarea, required=False)

class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ['sector_name']
        widgets = {
            'sector_name': forms.TextInput(attrs={'required': True, 'maxlength': 100}),
        }