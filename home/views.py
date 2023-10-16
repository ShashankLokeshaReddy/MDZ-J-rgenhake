from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import CustomerProfile
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        ust_id = request.POST['ust_id']
        email = request.POST['email']
        password = request.POST['password']
        unternehmensname = request.POST['unternehmensname']
        land = request.POST['land']
        address = request.POST['address']
        telefonnummer = request.POST['telefonnummer']
        ansprechpartner = request.POST['ansprechpartner']

        # Create a new user
        user = User.objects.create_user(username=ust_id, email=email, password=password)

        # Create a CustomerProfile instance associated with the user
        customer_profile = CustomerProfile.objects.create(
            ust_id=ust_id,
            unternehmensname=unternehmensname,
            land=land,
            address=address,
            email=email,
            telefonnummer=telefonnummer,
            ansprechpartner=ansprechpartner
        )

        # Redirect to the login page after successful registration
        return redirect('login')

    return render(request, 'registration/register.html')

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

def register(request):
    return render(request, 'accounts/register.html')

def login(request):
    return render(request, 'accounts/login.html')

def purchase(request):
    return render(request, 'pages/purchase.html')