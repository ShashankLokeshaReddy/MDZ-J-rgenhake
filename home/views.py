from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Akkuvariante, CustomerProfile
from .forms import UserRegisterForm
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def register(request):
    if request.method == 'POST':
        userRegisterForm = UserRegisterForm(request.POST)

        if userRegisterForm.is_valid():
            userRegisterForm.save()
            customerProfile = CustomerProfile(
                ust_id=userRegisterForm.cleaned_data['username'],
                email=userRegisterForm.cleaned_data['email'])
            customerProfile.save()
            return redirect('login')
        else:
            render(request, 'accounts/register.html', {'userRegisterForm': userRegisterForm})
    else:
        userRegisterForm = UserRegisterForm()
        return render(request, 'accounts/register.html', {'userRegisterForm': userRegisterForm})

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

def akkuvariante_list(request):
    akkuvarianten = Akkuvariante.objects.all()
    # akkuvarianten_list = []
    # for akkuvariante in akkuvarianten:
    #     akkuvarianten_list.append({
    #         'name': akkuvariante.name,
    #         # Include other fields as needed
    #     })
    print("akkuvarianten:", akkuvarianten)