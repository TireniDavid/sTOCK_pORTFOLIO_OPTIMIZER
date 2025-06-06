from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Portfolio

class CustomLoginForm(AuthenticationForm):
    username = forms. CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio

        fields = [
            'name', 'drag_percentage', 'rebalance_frequency', 
            'total_return', 'rebalance_bands', 'ticker', 'allocation'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'border p-2 rounded-md'}),
            'drag_percentage': forms.NumberInput(attrs={'class': 'border p-2 rounded-md'}),
            'rebalance_frequency': forms.Select(),
            'total_return': forms.CheckboxInput(attrs={'class': 'border p-2 rounded-md'}),
            'rebalance_bands': forms.CheckboxInput(attrs={'class': 'border p-2 rounded-md'}),
            'ticker': forms.TextInput(attrs={'class': 'border p-2 rounded-md'}),
            'allocation': forms.TextInput(attrs={'class': 'border p-2 rounded-md'}),
        }