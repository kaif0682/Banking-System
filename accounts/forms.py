from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Transaction

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

class WithdrawalForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12, 
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter amount to withdraw'
        })
    )