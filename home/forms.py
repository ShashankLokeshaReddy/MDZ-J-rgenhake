from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CustomerProfile
from crispy_forms.helper import FormHelper

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
class ProfileImageUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['image']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.field_class = 'form-control'

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.field_class = 'form-control form-control-sm'

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['unternehmensname', 'land', 'address', 'telefonnummer', 'ansprechpartner']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.field_class = 'form-control form-control-sm'