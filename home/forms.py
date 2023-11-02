from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CustomerProfile
from django.forms import ModelForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomerProfileRegisterForm(ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['ust_id', 'land', 'unternehmensname', 'address', 'email', 'telefonnummer', 'ansprechpartner']