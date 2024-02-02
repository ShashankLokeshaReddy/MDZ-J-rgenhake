from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import CustomerProfile, Akkuvariante, Kabelvariante, Schnittstelle, Color, UILabel, Image, Order, InCartItem, OrderItem, PreisListe
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileImageUpdateForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import re
import uuid
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv

@csrf_exempt
def register(request):
    ui_labels_data = get_ui_labels(request)
    firma = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'firma'), '')
    firma_adresse_1 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'firma-adresse-1'), '')
    firma_adresse_2 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'firma-adresse-2'), '')
    fon = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'fon'), '')
    fax = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'fax'), '')
    email = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'E-Mail'), '')
    webseite = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'webseite'), '')
    footer_copyright_info = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'footer-copyright-info'), '')

    if request.method == 'POST':
        userRegisterForm = UserRegisterForm(request.POST)

        if userRegisterForm.is_valid():
            userRegisterForm.save()
            return redirect('login')
        else:
            render(request, 'accounts/register.html', {
                'firma': firma,
                'firma_adresse_1': firma_adresse_1,
                'firma_adresse_2': firma_adresse_2,
                'fon': fon,
                'fax': fax,
                'email': email,
                'webseite': webseite,
                'footer_copyright_info': footer_copyright_info,
                })
    else:
        userRegisterForm = UserRegisterForm()
        return render(request, 'accounts/register.html', {
            'userRegisterForm': userRegisterForm,
            'firma': firma,
            'firma_adresse_1': firma_adresse_1,
            'firma_adresse_2': firma_adresse_2,
            'fon': fon,
            'fax': fax,
            'email': email,
            'webseite': webseite,
            'footer_copyright_info': footer_copyright_info,
            })

def index(request):
    customer_profiles = get_customer_profiles(request)
    colors = get_colors(request)
    ui_labels = get_ui_labels(request)
    image_paths = get_image_path(request)
    orders = get_orders(request)
    ui_labels_data = get_ui_labels(request)
    index_text = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'index_text'), '')
    firma = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'firma'), '')
    firma_adresse_1 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'firma-adresse-1'), '')
    firma_adresse_2 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'firma-adresse-2'), '')
    fon = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'fon'), '')
    fax = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'fax'), '')
    email = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'E-Mail'), '')
    webseite = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'webseite'), '')
    footer_copyright_info = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'footer-copyright-info'), '')

    return render(request, 'pages/index.html', {
        'customer_profiles': customer_profiles,
        'colors': colors,
        'image_paths': image_paths,
        'orders': orders,
        'in_cart_items': get_in_cart_items(request),
        'index_text':index_text,
        'firma': firma,
        'firma_adresse_1': firma_adresse_1,
        'firma_adresse_2': firma_adresse_2,
        'fon': fon,
        'fax': fax,
        'email': email,
        'webseite': webseite,
        'footer_copyright_info': footer_copyright_info,
    })

@login_required
def configurator(request):
    customer_profiles = get_customer_profiles(request)
    akkuvarianten = get_akkuvarianten(request)
    kabelvarianten = get_kabelvarianten(request)
    schnittstellen = get_schnittstellen(request)
    colors = get_colors(request)
    ui_labels = get_ui_labels(request)
    image_paths = get_image_path(request)
    orders = get_orders(request)
    preisliste = get_preisliste(request)
    ui_labels_data = get_ui_labels(request)
    firma = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'firma'), '')
    firma_adresse_1 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'firma-adresse-1'), '')
    firma_adresse_2 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'firma-adresse-2'), '')
    fon = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'fon'), '')
    fax = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'fax'), '')
    email = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'E-Mail'), '')
    webseite = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'webseite'), '')
    footer_copyright_info = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'footer-copyright-info'), '')

    for kabelvariante in kabelvarianten:
        kabelvariante['kabelvariante_image_path'] = str(kabelvariante['kabelvariante_image_path'])
        kabelvariante['masse_image_path'] = str(kabelvariante['masse_image_path'])
        kabelvariante['splits'] = str(kabelvariante['splits'])
        kabelvariante['main_part_min_length'] = str(kabelvariante['main_part_min_length'])
        kabelvariante['split_part_min_length'] = str(kabelvariante['split_part_min_length'])
        
    for schnittstelle in schnittstellen:
        schnittstelle['schnittstelle_image_path'] = str(schnittstelle['schnittstelle_image_path'])
        
    for preislist in preisliste:
        preislist['qty_1'] = str(preislist['qty_1'])
        preislist['qty_25'] = str(preislist['qty_25'])
        preislist['qty_50'] = str(preislist['qty_50'])
        preislist['qty_100'] = str(preislist['qty_100'])
        preislist['qty_250'] = str(preislist['qty_250'])
        preislist['qty_500'] = str(preislist['qty_500'])
        preislist['qty_1000'] = str(preislist['qty_1000'])      
        preislist['qty_2000'] = str(preislist['qty_2000'])     

    preisliste_json = json.dumps(preisliste)
    kabelvarianten_json = json.dumps(kabelvarianten)
    schnittstellen_json = json.dumps(schnittstellen)

    # print("kabelvariante type:",type(kabelvariante), type(kabelvariante_json))
    print("kabelvariante:",kabelvarianten)
    print("kabelvariante:",kabelvarianten_json)

    return render(request, 'pages/configurator.html', {
        'customer_profiles': customer_profiles,
        'akkuvarianten': akkuvarianten,
        'kabelvarianten': kabelvarianten_json,
        'schnittstellen': schnittstellen_json,
        'colors': colors,
        'image_paths': image_paths,
        'orders': orders,
        'in_cart_items': get_in_cart_items(request),
        'preisliste': preisliste_json,
        'firma': firma,
        'firma_adresse_1': firma_adresse_1,
        'firma_adresse_2': firma_adresse_2,
        'fon': fon,
        'fax': fax,
        'email': email,
        'webseite': webseite,
        'footer_copyright_info': footer_copyright_info,
    })

@login_required
def profile(request):
    ui_labels_data = get_ui_labels(request)
    firma = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'firma'), '')
    firma_adresse_1 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'firma-adresse-1'), '')
    firma_adresse_2 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'firma-adresse-2'), '')
    fon = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'fon'), '')
    fax = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'fax'), '')
    email = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'E-Mail'), '')
    webseite = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'webseite'), '')
    footer_copyright_info = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'footer-copyright-info'), '')

    if request.method == 'POST':
        profileImageUpdateForm = ProfileImageUpdateForm(
            request.POST, request.FILES, instance=request.user.customerprofile)
        userUpdateForm = UserUpdateForm(request.POST, instance=request.user)
        profileUpdateForm = ProfileUpdateForm(
            request.POST, instance=request.user.customerprofile)
        if profileImageUpdateForm.is_valid() and userUpdateForm.is_valid() and profileUpdateForm.is_valid():
            profileImageUpdateForm.save()
            userUpdateForm.save()
            profileUpdateForm.save()
            messages.success(request, f'Your profile changes have been saved!')
            return redirect('profile')
    else:
        profileImageUpdateForm = ProfileImageUpdateForm(instance=request.user.customerprofile)
        userUpdateForm = UserUpdateForm(instance=request.user)
        profileUpdateForm = ProfileUpdateForm(instance=request.user.customerprofile)

    context = {
        'i_form': profileImageUpdateForm,
        'u_form': userUpdateForm,
        'p_form': profileUpdateForm,
        'orders': get_orders(request),
        'in_cart_items': get_in_cart_items(request),
        'firma': firma,
        'firma_adresse_1': firma_adresse_1,
        'firma_adresse_2': firma_adresse_2,
        'fon': fon,
        'fax': fax,
        'email': email,
        'webseite': webseite,
        'footer_copyright_info': footer_copyright_info,
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
    ui_labels_data = get_ui_labels(request)
    firma = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'firma'), '')
    firma_adresse_1 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'firma-adresse-1'), '')
    firma_adresse_2 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'firma-adresse-2'), '')
    fon = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'fon'), '')
    fax = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'fax'), '')
    email = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'E-Mail'), '')
    webseite = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'webseite'), '')
    footer_copyright_info = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'footer-copyright-info'), '')

    for kabelvariante in kabelvarianten:
        kabelvariante['splits'] = int(kabelvariante['splits'])
        kabelvariante['main_part_min_length'] = int(kabelvariante['main_part_min_length'])
        kabelvariante['split_part_min_length'] = int(kabelvariante['split_part_min_length'])
        
    return render(request, 'pages/developer_mode.html', {
        'customer_profiles': customer_profiles,
        'akkuvarianten': akkuvarianten,
        'kabelvarianten': kabelvarianten,
        'schnittstellen': schnittstellen,
        'colors': colors,
        'ui_labels': ui_labels,
        'image_paths': image_paths,
        'orders': orders,
        'in_cart_items': get_in_cart_items(request),
        'firma': firma,
        'firma_adresse_1': firma_adresse_1,
        'firma_adresse_2': firma_adresse_2,
        'fon': fon,
        'fax': fax,
        'email': email,
        'webseite': webseite,
        'footer_copyright_info': footer_copyright_info,
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

@login_required
def orders(request):
    ui_labels_data = get_ui_labels(request)
    firma = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'firma'), '')
    firma_adresse_1 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'firma-adresse-1'), '')
    firma_adresse_2 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'firma-adresse-2'), '')
    fon = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'fon'), '')
    fax = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'fax'), '')
    email = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'E-Mail'), '')
    webseite = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'webseite'), '')
    footer_copyright_info = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'footer-copyright-info'), '')

    # Filter orders based on the current user's ust_id
    orders = Order.objects.filter(ust_id=request.user.customerprofile.ust_id).order_by('-order_date')
    user_orders = [{'order_number': order.order_number,
             'ust_id': order.ust_id,
             'order_date': order.order_date,
             'order_details': order.order_details,
             'order_status' : order.order_status,
             'total': sum([item.total for item in order.orderitem_set.all()]),
             'items': [{
                 'item_number': item.item_number,
                 'mit_120_Ohm_CAN_Bus_Widerstand': item.mit_120_Ohm_CAN_Bus_Widerstand,
                 'akkuvariante': item.akkuvariante,
                 'kabelvariante': item.kabelvariante,
                 'schnittstelle': item.schnittstelle,
                 'masse': item.masse,
                 'quantity': item.quantity,
                 'price': item.price,
                 'total': item.total
             } for item in order.orderitem_set.all()]
             } for order in orders]

    # Pagination for both tables
    page = request.GET.get('page', 1)
    paginator_orders = Paginator(user_orders, 10)

    try:
        user_orders = paginator_orders.page(page)
    except PageNotAnInteger:
        user_orders = paginator_orders.page(1)
    except EmptyPage:
        user_orders = paginator_orders.page(paginator_orders.num_pages)

    context = {
        'orders': user_orders,
        'firma': firma,
        'firma_adresse_1': firma_adresse_1,
        'firma_adresse_2': firma_adresse_2,
        'fon': fon,
        'fax': fax,
        'email': email,
        'webseite': webseite,
        'footer_copyright_info': footer_copyright_info,
    }

    return render(request, 'pages/orders.html', context)

@login_required
def purchase(request):
    ui_labels_data = get_ui_labels(request)
    firma = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'firma'), '')
    firma_adresse_1 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'firma-adresse-1'), '')
    firma_adresse_2 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'firma-adresse-2'), '')
    fon = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'fon'), '')
    fax = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'fax'), '')
    email = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'E-Mail'), '')
    webseite = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'webseite'), '')
    rabatt_text = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'rabatt_text'), '')
    footer_copyright_info = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'footer-copyright-info'), '')

    preisliste = get_preisliste(request)
    for preislist in preisliste:
        preislist['qty_1'] = str(preislist['qty_1'])
        preislist['qty_25'] = str(preislist['qty_25'])
        preislist['qty_50'] = str(preislist['qty_50'])
        preislist['qty_100'] = str(preislist['qty_100'])
        preislist['qty_250'] = str(preislist['qty_250'])
        preislist['qty_500'] = str(preislist['qty_500'])
        preislist['qty_1000'] = str(preislist['qty_1000'])      
        preislist['qty_2000'] = str(preislist['qty_2000'])     

    preisliste_json = json.dumps(preisliste)
    # Filter in cart items based on the current user's ust_id
    user_in_cart_items = InCartItem.objects.filter(ust_id=request.user.customerprofile.ust_id)

    # Pagination for both tables
    page = request.GET.get('page', 1)
    paginator_in_cart = Paginator(user_in_cart_items, 10)

    try:
        in_cart_items = paginator_in_cart.page(page)
    except PageNotAnInteger:
        in_cart_items = paginator_in_cart.page(1)
    except EmptyPage:
        in_cart_items = paginator_in_cart.page(paginator_in_cart.num_pages)

    context = {
        'in_cart_items': in_cart_items,
        'preisliste': preisliste_json,
        'firma': firma,
        'firma_adresse_1': firma_adresse_1,
        'firma_adresse_2': firma_adresse_2,
        'fon': fon,
        'fax': fax,
        'email': email,
        'webseite': webseite,
        'rabatt_text': rabatt_text,
        'footer_copyright_info': footer_copyright_info,
    }

    return render(request, 'pages/purchase.html', context)

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

def get_preisliste(request):
    preisliste = PreisListe.objects.all()
    data = [{'kabelvariante': preislist.kabelvariante,
             'gehause': preislist.gehause,
             'leitung': preislist.leitung,
             'lange': preislist.lange,
             'qty_1': preislist.qty_1,
             'qty_25': preislist.qty_25,
             'qty_50': preislist.qty_50,
             'qty_100': preislist.qty_100,
             'qty_250': preislist.qty_250,
             'qty_500': preislist.qty_500,
             'qty_1000': preislist.qty_1000,
             'qty_2000': preislist.qty_2000
             } for preislist in preisliste]

    return data # JsonResponse(data, safe=False)

def get_akkuvarianten(request):
    akkuvarianten = Akkuvariante.objects.all()
    data = [{'akkuvariante_name': akkuvariante.akkuvariante_name,
             'akkuvariante_image_path': akkuvariante.akkuvariante_image_path} for akkuvariante in akkuvarianten]
    print("get_akkuvarianten",data)
    return data # JsonResponse(data, safe=False)

def get_kabelvarianten(request):
    kabelvarianten = Kabelvariante.objects.all()
    data = [{'kabelvariante_name': kabelvariante.kabelvariante_name,
             'kabelvariante_image_path': kabelvariante.kabelvariante_image_path,
             'main_part_min_length': kabelvariante.main_part_min_length,
             'split_part_min_length': kabelvariante.split_part_min_length,
             'masse_image_path': kabelvariante.masse_image_path,
            #  'schnittstelle_image_path': kabelvariante.schnittstelle_image_path,
             'splits': kabelvariante.splits} for kabelvariante in kabelvarianten]
    return data # JsonResponse(data, safe=False)

def get_schnittstellen(request):
    schnittstellen = Schnittstelle.objects.all()
    data = [{'schnittstelle_name': schnittstelle.schnittstelle_name,
             'schnittstelle_image_path': schnittstelle.schnittstelle_image_path} for schnittstelle in schnittstellen]
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
    try:
        orders = Order.objects.filter(ust_id=request.user.customerprofile.ust_id)
        data = [{'order_number': order.order_number,
                'ust_id': order.ust_id,
                'order_date': order.order_date,
                'order_details': order.order_details,
                'order_status' : order.order_status,
                'items': [{
                    'item_number': item.item_number,
                    'mit_120_Ohm_CAN_Bus_Widerstand': item.mit_120_Ohm_CAN_Bus_Widerstand,
                    'akkuvariante': item.akkuvariante,
                    'kabelvariante': item.kabelvariante,
                    'schnittstelle': item.schnittstelle,
                    'masse': item.masse,
                    'quantity': item.quantity,
                    'price': item.price,
                    'total': item.total
                } for item in orders.orderitem_set.all()]
                } for order in orders]
    except Exception as e:
        print(f"Error getting user orders: {str(e)}")
        return []
    else:
        print("Successfully fetched user orders.")
        return data

def get_in_cart_items(request):
    inCartItems = InCartItem.objects.all()
    try:
        data = [{'item_number': inCartItem.item_number,
             'ust_id': inCartItem.ust_id,
             'akkuvariante': inCartItem.akkuvariante,
             'kabelvariante': inCartItem.kabelvariante,
             'schnittstelle ': inCartItem.schnittstelle,
             'masse ': inCartItem.masse,
             'quantity' : inCartItem.quantity,
             'price': inCartItem.price,
             'total': inCartItem.total} for inCartItem in inCartItems.filter(ust_id=request.user.customerprofile.ust_id)]
    except Exception as e:
        print(f"Error getting user in cart items: {str(e)}")
        return []
    else:
        print("Successfully fetched user in cart items.")
        return data

@require_POST
def cancel_order(request):
    try:
        json_data = json.loads(request.body)
        order_number = json_data['order_number']

        # Cancel the order with the given order_number
        Order.objects.filter(order_number=order_number).update(order_status='Cancelled')

        try:
            send_cancel_notification(request)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error sending notification about order cancellation: {str(e)}'})
        else:
            return JsonResponse({'success': True, 'message': 'Order cancelled successfully.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error cancelling order: {str(e)}'})

@require_POST
def order_again(request):
    try:
        json_data = json.loads(request.body)
        order_number = json_data['order_number']

        # Cancel the order with the given order_again
        Order.objects.filter(order_number=order_number).update(order_status='Ordered')

        try:
            send_reorder_notification(request)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error sending notification about reordering: {str(e)}'})
        else:
            return JsonResponse({'success': True, 'message': 'Ordered again successfully.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error reordering: {str(e)}'})

@require_POST
def delete_item(request):
    try:
        json_data = json.loads(request.body)
        item_number = json_data['item_number']

        # Delete the item with the given item_number
        InCartItem.objects.filter(item_number=item_number).delete()

        return JsonResponse({'success': True, 'message': 'Cart item deleted successfully.'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error deleting cart item: {str(e)}'})

@require_POST
def create_order_with_items(request):
    try:
        json_data = json.loads(request.body)
        items_in_order = json_data['items_in_order']
        ust_id = request.user.customerprofile.ust_id
        order_status = 'Ordered'

        # Print the request data to the console or log file
        print(f"Received json_data request data: {json_data}")
        print(f"Received items_in_order request data: {items_in_order}")

        # Create order object
        order = Order.objects.create(ust_id=ust_id, order_status=order_status)
        order.save()

        try:
            for entry in items_in_order:
                print(f"Received entry: {entry}")
                item_number = entry['item_number']
                akkuvariante = entry['akkuvariante']
                mit_120_Ohm_CAN_Bus_Widerstand = entry['mit_120_Ohm_CAN_Bus_Widerstand']
                kabelvariante = entry['kabelvariante']
                schnittstelle = entry['schnittstelle']
                masse = entry['masse']
                price = entry['price']
                quantity = entry['quantity']
                total = entry['total']

                OrderItem.objects.create(order=order, ust_id=ust_id, akkuvariante=akkuvariante, mit_120_Ohm_CAN_Bus_Widerstand=mit_120_Ohm_CAN_Bus_Widerstand, kabelvariante=kabelvariante, schnittstelle=schnittstelle, masse=masse, quantity=quantity, price=price, total=total)
                InCartItem.objects.filter(item_number=item_number).delete()
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error creating order items: {str(e)} {order}'})

        print("Update orders success")
        messages.success(request, f'Your orders have been submitted!')
        return JsonResponse({'success': True, 'message': 'Orders updated successfully'})

    except Exception as e:
        print("Update orders not success")
        print(f"Error updating orders: {str(e)}")
        return JsonResponse({'success': False, 'message': f'Error creating orders: {str(e)}'})

@csrf_exempt
@require_POST
def add_item_to_cart(request):
    try:
        json_data = json.loads(request.body)
        json_string = json.dumps(json_data, ensure_ascii=False)
        match = re.search(r'\d+\.\d+', json_data['preis'])

        ust_id = request.user.customerprofile.ust_id
        akkuvariante = json_data.get('akkuvarianteName', '')
        CAN_Bus = json_data.get('CAN_Bus', '')
        kabelvariante = json_data.get('kabelvariante', '')
        schnittstelle = ', '.join(json_data.get('schnittstelle', []))
        masse = ', '.join(json_data.get('masse', []))
        price = float(match.group())

        # Check if the item with matching values exists
        existing_item = InCartItem.objects.filter(
            ust_id=ust_id,
            akkuvariante=akkuvariante,
            mit_120_Ohm_CAN_Bus_Widerstand=CAN_Bus,
            kabelvariante=kabelvariante,
            schnittstelle=schnittstelle,
            masse=masse,
            price=price
        ).first()

        if existing_item:
            # Item already exists, update quantity
            existing_item.quantity += 1
            existing_item.total = existing_item.quantity * existing_item.price
            existing_item.save()
        else:
            # Item does not exist, create a new entry
            item_number = str(uuid.uuid4())
            InCartItem.objects.create(
                item_number=item_number,
                ust_id=ust_id,
                akkuvariante=akkuvariante,
                mit_120_Ohm_CAN_Bus_Widerstand=CAN_Bus,
                kabelvariante=kabelvariante,
                schnittstelle=schnittstelle,
                masse=masse,
                quantity=1,
                price=price,
                total=price
            )

        return JsonResponse({'success': True, 'message': 'Cart item updated/created successfully.'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error updating/creating cart item: {str(e)}'})
    try:
        json_data = json.loads(request.body)
        json_string = json.dumps(json_data, ensure_ascii=False)
        match = re.search(r'\d+\.\d+', json_data['preis'])

        ust_id = request.user.customerprofile.ust_id
        item_number = str(uuid.uuid4())
        akkuvariante = json_data.get('akkuvarianteName', '')
        CAN_Bus = json_data.get('CAN_Bus', '')
        kabelvariante = json_data.get('kabelvariante', '')
        schnittstelle = ', '.join(json_data.get('schnittstelle', []))
        masse = ', '.join(json_data.get('masse', []))
        price = float(match.group())
        
        inCartItems = InCartItem.objects.all()
        data = [{'item_number': inCartItem.item_number,
             'ust_id': inCartItem.ust_id,
             'akkuvariante': inCartItem.akkuvariante,
             'mit_120_Ohm_CAN_Bus_Widerstand':inCartItem.mit_120_Ohm_CAN_Bus_Widerstand,
             'kabelvariante': inCartItem.kabelvariante,
             'schnittstelle ': inCartItem.schnittstelle,
             'masse ': inCartItem.masse,
             'quantity' : inCartItem.quantity,
             'price': inCartItem.price,
             'total': inCartItem.total} for inCartItem in inCartItems.filter(ust_id=ust_id)]
    
        cart_item = InCartItem.objects.create(
            item_number=item_number,
            ust_id=ust_id,
            akkuvariante=akkuvariante,
            mit_120_Ohm_CAN_Bus_Widerstand=CAN_Bus,
            kabelvariante=kabelvariante,
            schnittstelle=schnittstelle,
            masse=masse,
            quantity=1,
            price=price,
            total=price
        )

        return JsonResponse({'success': True, 'message': 'Cart item created successfully.'}, status=201)

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error creating cart item: {str(e)}'})

def send_cancel_notification(request):
    json_data = json.loads(request.body)
    order_number = json_data['order_number']

    order = Order.objects.filter(order_number=order_number, ust_id=request.user.customerprofile.ust_id).first()

    subject = f"Order #{order.order_number} has been cancelled!"
    body = f"""
    Your order #{order.order_number} has been cancelled.
    """

    send_email_notification(request, subject, body)
    return

def send_reorder_notification(request):
    json_data = json.loads(request.body)
    order_number = json_data['order_number']

    order = Order.objects.filter(order_number=order_number, ust_id=request.user.customerprofile.ust_id).first()

    subject = f"Order #{order.order_number} has been reordered!"
    body = f"""
    Your cancelled order #{order.order_number} has been reordered again.
    """
    send_email_notification(request, subject, body)
    return

def send_email_notification(request, subject, body):
    email_sender = 'jurgenhaketest@gmail.com'
    email_password = 'azuexffmhvurppvu'
    email_receiver = request.user.email

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

@require_POST
def upload_special_solution(request):
    try:
        # uploaded_file = request.FILES.get('specialfile')
        # special_order = SpecialOrder(uploaded_file=uploaded_file)
        # special_order.save()

        return JsonResponse({'message': 'File uploaded successfully'})

    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'})