from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms. CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class PortfolioForm(forms.Form):
    portfolio_name = forms.CharField(label="Portfolio Name", max_length=100, widget=forms.TextInput())
    drag_percentage = forms.FloatField(label="Drag %", initial=0, widget=forms.NumberInput())
    rebalance_frequency = forms.ChoiceField(
        label="Rebalance", choices=[('Yearly', 'Yearly'), ('Quarterly', 'Quarterly'), ('Monthly', 'Monthly')],
        widget=forms.Select()
    )
    total_return = forms.BooleanField(label="Total return", required=False, widget=forms.CheckboxInput())
    rebalance_bands = forms.BooleanField(label="Rebalance bands", required=False, widget=forms.CheckboxInput())
    ticker = forms.CharField(label="Ticker", max_length=10, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    allocation = forms.FloatField(label="Allocation %", initial=0, widget=forms.NumberInput())
