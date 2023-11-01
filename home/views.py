from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import CustomerProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CustomerProfileRegisterForm, UserRegisterForm
import logging
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def register(request):
    if request.method == 'POST':
        userRegisterForm = UserRegisterForm(request.POST)

        if userRegisterForm.is_valid():
            userRegisterForm.save()
            return redirect('login')
        else:
            render(request, 'accounts/register.html', {'userRegisterForm': userRegisterForm, 'customerProfileRegisterForm': customerProfileRegisterForm})
    else:
        userRegisterForm = UserRegisterForm()
        customerProfileRegisterForm = CustomerProfileRegisterForm()
        return render(request, 'accounts/register.html', {'userRegisterForm': userRegisterForm, 'customerProfileRegisterForm': customerProfileRegisterForm})

def user_login(request):
    if request.method == 'POST':
        ust_id = request.POST['ust_id']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=ust_id, password=password)

        if user is not None:
            login(request, user)  # Log in the user
            return redirect('dashboard')  # Redirect to the dashboard page after successful login
        else:
            # Authentication failed, handle the error (e.g., show an error message)
            pass

    return render(request, 'accounts/login.html')
# Create your views here.

def index(request):
    # Page from the theme 
    return render(request, 'pages/index.html')

def login(request):
    return render(request, 'accounts/login.html')

def purchase(request):
    return render(request, 'pages/purchase.html')