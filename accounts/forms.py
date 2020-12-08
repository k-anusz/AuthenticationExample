from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput
from .models import City
from .models import Bank
from .models import BankAccount


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# form for city name input
class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name': TextInput(attrs={'class': 'input form-control', 'placeholder': 'City Name'})}


# form for bank input
class BankForm(ModelForm):
    class Meta:
        model = Bank
        fields = ['userId', 'bankName', 'balance', 'startBal']
        widgets = {'bankName': TextInput(attrs={'class': 'input form-control', 'placeholder': 'Bank Name'}),
                   'balance': TextInput(attrs={'class': 'input form-control', 'placeholder': 'Balance'})}


# form for account transaction input
class AccountForm(ModelForm):
    class Meta:
        model = BankAccount
        fields = ['bankId', 'transactionName', 'transactionAmount']
        widgets = {'transactionName': TextInput(attrs={'class': 'input form-control', 'placeholder': 'Transaction Name'}),
                   'transactionAmount': TextInput(attrs={'class': 'input form-control', 'placeholder': 'Amount'})}
