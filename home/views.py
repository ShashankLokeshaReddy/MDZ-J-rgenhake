from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import CustomerProfile, Akkuvariante, Kabelvariante, Schnittstelle, Color, UILabel, Image
from .forms import CustomerProfileRegisterForm, UserRegisterForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

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

def index(request):
    customer_profiles = get_customer_profiles(request)
    akkuvarianten = get_akkuvarianten(request)
    kabelvarianten = get_kabelvarianten(request)
    schnittstellen = get_schnittstellen(request)
    colors = get_colors(request)
    ui_labels = get_ui_labels(request)
    image_paths = get_image_path(request)
    print("kabelvarianten in index", kabelvarianten)
    for kabelvariante in kabelvarianten:
        kabelvariante['splits'] = int(kabelvariante['splits'])
        kabelvariante['main_part_min_length'] = int(kabelvariante['main_part_min_length'])
        kabelvariante['main_part_max_length'] = int(kabelvariante['main_part_max_length'])
        kabelvariante['split_part_min_length'] = int(kabelvariante['split_part_min_length'])
        kabelvariante['split_part_max_length'] = int(kabelvariante['split_part_max_length'])
        kabelvariante['kabel_price_per_meter'] = float(kabelvariante['kabel_price_per_meter'])

    return render(request, 'pages/index.html', {
        'customer_profiles': customer_profiles,
        'akkuvarianten': akkuvarianten,
        'kabelvarianten': kabelvarianten,
        'schnittstellen': schnittstellen,
        'colors': colors,
        'ui_labels': ui_labels,
        'image_paths': image_paths,
    })

def purchase(request):
    return render(request, 'pages/purchase.html')

def get_customer_profiles(request):
    customer_profiles = CustomerProfile.objects.all()
    data = [{'ust_id': profile.ust_id,
             'unternehmensname': profile.unternehmensname,
             'land': profile.land,
             'address': profile.address,
             'email': profile.email,
             'telefonnummer': profile.telefonnummer,
             'ansprechpartner': profile.ansprechpartner} for profile in customer_profiles]
    return JsonResponse(data, safe=False)

def get_akkuvarianten(request):
    akkuvarianten = Akkuvariante.objects.all()
    data = [{'akkuvariante_name': akkuvariante.akkuvariante_name,
             'akkuvariante_image_path': akkuvariante.akkuvariante_image_path,
             'akkuvariante_price': akkuvariante.akkuvariante_price} for akkuvariante in akkuvarianten]
    print("get_akkuvarianten",data)
    return data # JsonResponse(data, safe=False)

def get_kabelvarianten(request):
    kabelvarianten = Kabelvariante.objects.all()
    data = [{'kabelvariante_name': kabelvariante.kabelvariante_name,
             'kabelvariante_image_path': kabelvariante.kabelvariante_image_path,
             'main_part_min_length': kabelvariante.main_part_min_length,
             'main_part_max_length': kabelvariante.main_part_max_length,
             'split_part_min_length': kabelvariante.split_part_min_length,
             'split_part_max_length': kabelvariante.split_part_max_length,
             'masse_image_path': kabelvariante.masse_image_path,
             'schnittstelle_image_path': kabelvariante.schnittstelle_image_path,
             'splits': kabelvariante.splits,
             'kabel_price_per_meter': kabelvariante.kabel_price_per_meter} for kabelvariante in kabelvarianten]
    return data # JsonResponse(data, safe=False)

def get_schnittstellen(request):
    schnittstellen = Schnittstelle.objects.all()
    data = [{'schnittstelle_name': schnittstelle.schnittstelle_name,
             'schnittstelle_image_path': schnittstelle.schnittstelle_image_path,
             'schnittstelle_price': schnittstelle.schnittstelle_price} for schnittstelle in schnittstellen]
    return data # JsonResponse(data, safe=False)

def get_colors(request):
    colors = Color.objects.all()
    data = [{'color_name': color.color_name} for color in colors]
    return data # JsonResponse(data, safe=False)

def get_ui_labels(request):
    ui_labels = UILabel.objects.all()
    data = [{'label_name': label.label_name} for label in ui_labels]
    return data # JsonResponse(data, safe=False)

def get_image_path(request):
    images = Image.objects.all()
    data = [{'image_path': image.image_path} for image in images]
    print("get_image_path",data)
    return data # JsonResponse(data, safe=False)

def get_orders(request):
    orders = Order.objects.all()
    data = [{'order_number': order.order_number,
             'ust_id': order.ust_id,
             'order_date': order.order_date,
             'order_details': order.order_details,
             'price': order.price} for order in orders]
    print("get_image_path",data)
    return data