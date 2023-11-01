from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Akkuvariante
from .forms import CustomerProfileRegisterForm, UserRegisterForm
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

# Create your views here.

def index(request):
    # Page from the theme 
    return render(request, 'pages/index.html')

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