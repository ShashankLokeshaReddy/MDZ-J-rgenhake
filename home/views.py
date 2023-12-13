from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import CustomerProfile, Akkuvariante, Kabelvariante, Schnittstelle, Color, UILabel, Image, Order
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@csrf_exempt
def register(request):
    if request.method == 'POST':
        userRegisterForm = UserRegisterForm(request.POST)

        if userRegisterForm.is_valid():
            userRegisterForm.save()
            return redirect('login')
        else:
            render(request, 'accounts/register.html', {'userRegisterForm': userRegisterForm})
    else:
        userRegisterForm = UserRegisterForm()
        return render(request, 'accounts/register.html', {'userRegisterForm': userRegisterForm})

def index(request):
    customer_profiles = get_customer_profiles(request)
    akkuvarianten = get_akkuvarianten(request)
    kabelvarianten = get_kabelvarianten(request)
    schnittstellen = get_schnittstellen(request)
    colors = get_colors(request)
    ui_labels = get_ui_labels(request)
    image_paths = get_image_path(request)
    orders = get_orders(request)
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
        'orders': orders,
    })

@login_required
def profile(request):
    if request.method == 'POST':
        userUpdateForm = UserUpdateForm(request.POST, instance=request.user)
        profileUpdateForm = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.customerprofile)
        if userUpdateForm.is_valid() and profileUpdateForm.is_valid():
            userUpdateForm.save()
            profileUpdateForm.save()
            messages.success(request, f'Your profile changes have been saved!')
            return redirect('profile')
    else:
        userUpdateForm = UserUpdateForm(instance=request.user)
        profileUpdateForm = ProfileUpdateForm(instance=request.user.customerprofile)

    context = {
        'u_form': userUpdateForm,
        'p_form': profileUpdateForm
    }
    return render(request, 'pages/profile.html', context)

@login_required(login_url='/login/')
@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def developer_mode(request):
    customer_profiles = get_customer_profiles(request)
    akkuvarianten = get_akkuvarianten(request)
    kabelvarianten = get_kabelvarianten(request)
    schnittstellen = get_schnittstellen(request)
    colors = get_colors(request)
    ui_labels = get_ui_labels(request)
    image_paths = get_image_path(request)
    orders = get_orders(request)
    for kabelvariante in kabelvarianten:
        kabelvariante['splits'] = int(kabelvariante['splits'])
        kabelvariante['main_part_min_length'] = int(kabelvariante['main_part_min_length'])
        kabelvariante['main_part_max_length'] = int(kabelvariante['main_part_max_length'])
        kabelvariante['split_part_min_length'] = int(kabelvariante['split_part_min_length'])
        kabelvariante['split_part_max_length'] = int(kabelvariante['split_part_max_length'])
        kabelvariante['kabel_price_per_meter'] = float(kabelvariante['kabel_price_per_meter'])

    return render(request, 'pages/developer_mode.html', {
        'customer_profiles': customer_profiles,
        'akkuvarianten': akkuvarianten,
        'kabelvarianten': kabelvarianten,
        'schnittstellen': schnittstellen,
        'colors': colors,
        'ui_labels': ui_labels,
        'image_paths': image_paths,
        'orders': orders,
    })

# @login_required(login_url='/login/')
# @user_passes_test(lambda u: u.is_superuser, login_url='/login/')
@require_POST
def update_colors(request):
    try:
        json_data = json.loads(request.body)

        for entry in json_data:
            color_name = entry['color_name']
            color_value = entry['color_value']

            if color_value == '':
                # If color value is empty, delete the entry from the database
                Color.objects.filter(color_name=color_name).delete()
            else:
                # Try to update the existing entry
                result = Color.objects.filter(color_name=color_name).update(color_value=color_value)

                # If no rows were updated, create a new entry
                if result == 0:
                    Color.objects.create(color_name=color_name, color_value=color_value)

        # Fetch and return the updated colors
        updated_colors = get_colors_dict()
        return JsonResponse({'success': True, 'message': 'Color values updated successfully.', 'colors': updated_colors})

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error updating color values: {str(e)}'})

def get_colors_dict():
    # Helper function to fetch colors as a dictionary
    colors = Color.objects.all()
    return {color.color_name: color.color_value for color in colors}

def purchase(request):
    return render(request, 'pages/purchase.html')

def get_customer_profiles(request):
    customer_profiles = CustomerProfile.objects.all()
    data = [{'ust_id': profile.user.username,
             'unternehmensname': profile.unternehmensname,
             'land': profile.land,
             'address': profile.address,
             'email': profile.user.email,
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
    data = [{'color_name': color.color_name, 'color_value': color.color_value} for color in colors]
    return data # JsonResponse(data, safe=False)

def colors_url(request):
    if request.method == 'GET':
        colors_data = get_colors(request)
        formatted_data = {color['color_name']: color['color_value'] for color in colors_data}

        return JsonResponse(formatted_data)
    else:
        return JsonResponse({'error': 'Invalid request method'})

def get_ui_labels(request):
    ui_labels = UILabel.objects.all()
    data = [{'label_key': label.label_key, 'label_value': label.label_value} for label in ui_labels]
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