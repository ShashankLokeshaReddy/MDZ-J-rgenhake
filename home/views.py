from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import CustomerProfile, Akkuvariante, Kabelvariante, Schnittstelle, Color, UILabel, Image, Order, InCartItem, OrderItem, PreisListe, SpezielleBestellung
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileImageUpdateForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import re
import uuid
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .notifications import NotificationService
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views

def logout_view(request):
    logout(request)
    messages.success(request, f'Erfolgreich abgemeldet!')
    return redirect('/') 

@login_required
def check_login_status(request):
    """
    View to check the login status of the user.
    """
    return JsonResponse({'logged_in': True})

class CustomLoginView(auth_views.LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ui_labels_data = self.__get_ui_labels()
        title = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Titel'), '')
        context.update({
            'title': title
        })
        return context

    def __get_ui_labels(self):
        ui_labels = UILabel.objects.all()
        data = [{'label_key': label.label_key, 'label_value': label.label_value} for label in ui_labels]
        return data # JsonResponse(data, safe=False)


@csrf_exempt
def register(request):
    ui_labels_data = get_ui_labels(request)
    title = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Titel'), '')
    firma = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Firma'), '')
    firma_adresse_1 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Firma_Adresse_1'), '')
    firma_adresse_2 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Firma_Adresse_2'), '')
    fon = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Fon'), '')
    fax = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Fax'), '')
    email = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Info_Email'), '')
    webseite = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Webseite'), '')
    footer_copyright_info = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Footer_Copyright_Info'), '')

    if request.method == 'POST':
        userRegisterForm = UserRegisterForm(request.POST)

        if userRegisterForm.is_valid():
            userRegisterForm.save()
            return redirect('login')
        else:
            render(request, 'accounts/register.html', {
                'title': title,
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
            'title': title,
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
    image_paths = get_image_path(request)
    orders = get_orders(request)
    ui_labels_data = get_ui_labels(request)
    title = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Titel'), '')
    index_text = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Index_Text'), '')
    firma = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Firma'), '')
    firma_adresse_1 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Firma_Adresse_1'), '')
    firma_adresse_2 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Firma_Adresse_2'), '')
    fon = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Fon'), '')
    fax = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Fax'), '')
    email = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Info_Email'), '')
    webseite = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Webseite'), '')
    footer_copyright_info = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Footer_Copyright_Info'), '')

    return render(request, 'pages/index.html', {
        'title': title,
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

def konfigurator(request):
    customer_profiles = get_customer_profiles(request)
    akkuvarianten = get_akkuvarianten(request)
    kabelvarianten = get_kabelvarianten(request)
    schnittstellen = get_schnittstellen(request)
    colors = get_colors(request)
    image_paths = get_image_path(request)
    orders = get_orders(request)
    preisliste = get_preisliste(request)
    ui_labels_data = get_ui_labels(request)
    title = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Titel'), '')
    firma = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Firma'), '')
    firma_adresse_1 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Firma_Adresse_1'), '')
    firma_adresse_2 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Firma_Adresse_2'), '')
    fon = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Fon'), '')
    fax = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Fax'), '')
    email = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Info_Email'), '')
    webseite = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Webseite'), '')
    footer_copyright_info = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Footer_Copyright_Info'), '')

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
        'title': title,
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
def profil(request):
    ui_labels_data = get_ui_labels(request)
    title = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Titel'), '')
    firma = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Firma'), '')
    firma_adresse_1 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Firma_Adresse_1'), '')
    firma_adresse_2 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Firma_Adresse_2'), '')
    fon = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Fon'), '')
    fax = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Fax'), '')
    email = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Info_Email'), '')
    webseite = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Webseite'), '')
    footer_copyright_info = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Footer_Copyright_Info'), '')

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
            messages.success(request, f'Deine Profiländerungen wurden gespeichert!')
            return redirect('profil')
    else:
        profileImageUpdateForm = ProfileImageUpdateForm(instance=request.user.customerprofile)
        userUpdateForm = UserUpdateForm(instance=request.user)
        profileUpdateForm = ProfileUpdateForm(instance=request.user.customerprofile)

    context = {
        'title': title,
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
    title = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Titel'), '')
    firma = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Firma'), '')
    firma_adresse_1 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Firma_Adresse_1'), '')
    firma_adresse_2 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Firma_Adresse_2'), '')
    fon = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Fon'), '')
    fax = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Fax'), '')
    email = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Info_Email'), '')
    webseite = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Webseite'), '')
    footer_copyright_info = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Footer_Copyright_Info'), '')

    # Filter orders based on the current user's benutzername
    orders = Order.objects.filter(benutzername=request.user.customerprofile.benutzername).order_by('-order_datum')
    user_orders = [{'order_nummer': order.order_nummer,
             'benutzername': order.benutzername,
             'order_datum': order.order_datum,
             'bestelldetails': order.bestelldetails,
             'order_status' : order.order_status,
             'gesamt': sum([item.gesamt for item in order.orderitem_set.all()]),
             'items': [{
                 'item_nummer': item.item_nummer,
                 'mit_120_Ohm_CAN_Bus_Widerstand': item.mit_120_Ohm_CAN_Bus_Widerstand,
                 'akkuvariante': item.akkuvariante,
                 'kabelvariante': item.kabelvariante,
                 'schnittstelle': item.schnittstelle,
                 'masse': item.masse,
                 'menge': item.menge,
                 'original_preis': item.original_preis,
                 'reduzierter_preis': item.reduzierter_preis,
                 'gesamt': item.gesamt
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
        'title': title,
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
def warenkorb(request):
    ui_labels_data = get_ui_labels(request)
    title = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Titel'), '')
    firma = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Firma'), '')
    firma_adresse_1 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Firma_Adresse_1'), '')
    firma_adresse_2 = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Firma_Adresse_2'), '')
    fon = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Fon'), '')
    fax = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Fax'), '')
    email = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Info_Email'), '')
    webseite = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Webseite'), '')
    warenkorb_text = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Warenkorb_Text'), '')
    footer_copyright_info = next((label['label_value'] for label in ui_labels_data if label['label_key'] == 'Footer_Copyright_Info'), '')

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
    # Filter in cart items based on the current user's benutzername
    user_in_cart_items = InCartItem.objects.filter(benutzername=request.user.customerprofile.benutzername)

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
        'title': title,
        'in_cart_items': in_cart_items,
        'preisliste': preisliste_json,
        'firma': firma,
        'firma_adresse_1': firma_adresse_1,
        'firma_adresse_2': firma_adresse_2,
        'fon': fon,
        'fax': fax,
        'email': email,
        'webseite': webseite,
        'warenkorb_text': warenkorb_text,
        'footer_copyright_info': footer_copyright_info,
    }

    return render(request, 'pages/purchase.html', context)

def get_customer_profiles(request):
    customer_profiles = CustomerProfile.objects.all()
    data = [{'benutzername': profile.user.username,
             'unternehmensname': profile.unternehmensname,
             'land': profile.land,
             'adresse': profile.adresse,
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
    data = [{'image_path': image.general_image_path} for image in images]
    print("get_image_path",data)
    return data # JsonResponse(data, safe=False)

def get_orders(request):
    try:
        orders = Order.objects.filter(benutzername=request.user.customerprofile.benutzername)
        data = [{'order_nummer': order.order_nummer,
                'benutzername': order.benutzername,
                'order_datum': order.order_datum,
                'bestelldetails': order.bestelldetails,
                'order_status' : order.order_status,
                'items': [{
                    'item_nummer': item.item_nummer,
                    'mit_120_Ohm_CAN_Bus_Widerstand': item.mit_120_Ohm_CAN_Bus_Widerstand,
                    'akkuvariante': item.akkuvariante,
                    'kabelvariante': item.kabelvariante,
                    'schnittstelle': item.schnittstelle,
                    'masse': item.masse,
                    'menge': item.menge,
                    'original_preis': item.original_preis,
                    'reduzierter_preis': item.reduzierter_preis,
                    'gesamt': item.gesamt
                } for item in order.orderitem_set.all()]
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
        data = [{'item_nummer': inCartItem.item_nummer,
             'benutzername': inCartItem.benutzername,
             'akkuvariante': inCartItem.akkuvariante,
             'kabelvariante': inCartItem.kabelvariante,
             'schnittstelle ': inCartItem.schnittstelle,
             'masse ': inCartItem.masse,
             'menge' : inCartItem.menge,
             'original_preis': inCartItem.original_preis,
             'reduzierter_preis': inCartItem.reduzierter_preis,
             'gesamt': inCartItem.gesamt} for inCartItem in inCartItems.filter(benutzername=request.user.customerprofile.benutzername)]
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
        order_nummer = json_data['order_nummer']

        # Cancel the order with the given order_nummer
        Order.objects.filter(order_nummer=order_nummer).update(order_status='Abgesagt')

        try:
            notificationService = NotificationService()
            notificationService.send_cancel_notification(request)
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
        order_nummer = json_data['order_nummer']

        # Cancel the order with the given order_again
        Order.objects.filter(order_nummer=order_nummer).update(order_status='Bestellt')

        try:
            notificationService = NotificationService()
            notificationService.send_reorder_notification(request)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Fehler beim Senden der Benachrichtigung über die Nachbestellung: {str(e)}'})
        else:
            messages.success(request, f'Wieder erfolgreich bestellt.')
            return JsonResponse({'success': True, 'message': 'Wieder erfolgreich bestellt.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Fehler beim Nachbestellen: {str(e)}'})

@require_POST
def delete_item(request):
    try:
        json_data = json.loads(request.body)
        item_nummer = json_data['item_nummer']

        # Delete the item with the given item_nummer
        InCartItem.objects.filter(item_nummer=item_nummer).delete()

        return JsonResponse({'success': True, 'message': 'Warenkorbartikel erfolgreich gelöscht.'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Fehler beim Löschen des Warenkorbartikels: {str(e)}'})

@require_POST
def create_order_with_items(request):
    ui_labels_data = get_ui_labels(request)
    try:
        json_data = json.loads(request.body)
        items_in_order = json_data['items_in_order']
        benutzername = request.user.customerprofile.benutzername
        order_status = 'Bestellt'

        # Print the request data to the console or log file
        print(f"Received json_data request data: {json_data}")
        print(f"Received items_in_order request data: {items_in_order}")

        # Create order object
        order = Order.objects.create(benutzername=benutzername, order_status=order_status)
        order.save()

        try:
            for entry in items_in_order:
                print(f"Received entry: {entry}")
                item_nummer = entry['item_nummer']
                akkuvariante = entry['akkuvariante']
                mit_120_Ohm_CAN_Bus_Widerstand = entry['mit_120_Ohm_CAN_Bus_Widerstand']
                kabelvariante = entry['kabelvariante']
                schnittstelle = entry['schnittstelle']
                masse = entry['masse']
                original_preis = entry['original_preis'].replace(',', '.')
                reduzierter_preis = entry['reduzierter_preis'].replace(',', '.')
                menge = entry['menge']
                gesamt = entry['gesamt']

                OrderItem.objects.create(order=order, benutzername=benutzername, akkuvariante=akkuvariante, mit_120_Ohm_CAN_Bus_Widerstand=mit_120_Ohm_CAN_Bus_Widerstand, kabelvariante=kabelvariante, schnittstelle=schnittstelle, masse=masse, menge=menge, original_preis=original_preis, reduzierter_preis=reduzierter_preis, gesamt=gesamt)
                InCartItem.objects.filter(item_nummer=item_nummer).delete()
            notificationService = NotificationService()
            notificationService.send_order_created_notification(request, order, ui_labels_data)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Fehler beim Erstellen von Auftragspositionen: {str(e)} {order}'})

        print("Update orders success")
        messages.success(request, f'Ihre Bestellungen wurden übermittelt!')
        return JsonResponse({'success': True, 'message': 'Bestellungen erfolgreich aktualisiert'})

    except Exception as e:
        print("Update orders not success")
        print(f"Error updating orders: {str(e)}")
        return JsonResponse({'success': False, 'message': f'Fehler beim Erstellen von Bestellungen: {str(e)}'})

@require_POST
def create_offer_request_with_items(request):
    ui_labels_data = get_ui_labels(request)
    try:
        json_data = json.loads(request.body)
        items_in_order = json_data['items_in_order']
        benutzername = request.user.customerprofile.benutzername
        order_status = 'Angebot angefordert'

        # Print the request data to the console or log file
        print(f"Received json_data request data: {json_data}")
        print(f"Received items_in_order request data: {items_in_order}")

        # Create order object
        order = Order.objects.create(benutzername=benutzername, order_status=order_status)
        order.save()

        try:
            for entry in items_in_order:
                print(f"Received entry: {entry}")
                item_nummer = entry['item_nummer']
                akkuvariante = entry['akkuvariante']
                mit_120_Ohm_CAN_Bus_Widerstand = entry['mit_120_Ohm_CAN_Bus_Widerstand']
                kabelvariante = entry['kabelvariante']
                schnittstelle = entry['schnittstelle']
                masse = entry['masse']
                original_preis = entry['original_preis'].replace(',', '.')
                reduzierter_preis = entry['reduzierter_preis'].replace(',', '.')
                menge = entry['menge']
                gesamt = entry['gesamt']

                OrderItem.objects.create(order=order, benutzername=benutzername, akkuvariante=akkuvariante, mit_120_Ohm_CAN_Bus_Widerstand=mit_120_Ohm_CAN_Bus_Widerstand, kabelvariante=kabelvariante, schnittstelle=schnittstelle, masse=masse, menge=menge, original_preis=original_preis, reduzierter_preis=reduzierter_preis, gesamt=gesamt)
                InCartItem.objects.filter(item_nummer=item_nummer).delete()
            notificationService = NotificationService()
            notificationService.send_offer_requested_notification(request, order, ui_labels_data)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Fehler beim Erstellen von Auftragspositionen: {str(e)}'})

        print("Offer request create success")
        messages.success(request, f'Ihre Angebotsanfrage wurde übermittelt!')
        return JsonResponse({'success': True, 'message': 'Angebotsanfrage erfolgreich erstellt'})

    except Exception as e:
        print("Offer request create not success")
        print(f"Error creating offer request: {str(e)}")
        return JsonResponse({'success': False, 'message': f'Fehler beim Erstellen einer Angebotsanfrage: {str(e)}'})

@csrf_exempt
@require_POST
def add_item_to_cart(request):
    try:
        json_data = json.loads(request.body)
        json_string = json.dumps(json_data, ensure_ascii=False)
        match = re.search(r'\d+\.\d+', json_data['preis'])
        if not request.user.is_authenticated:
            login_url = reverse('login')  # Assuming you have a named URL pattern for the login page
            messages.warning(request, f'Um eine Bestellung aufzugeben, müssen Sie sich anmelden!')
            return JsonResponse({'message': 'You need to login to place an order', 'login_url': login_url})        
        else:
            benutzername = request.user.customerprofile.benutzername
            akkuvariante = json_data.get('akkuvarianteName', '')
            CAN_Bus = json_data.get('CAN_Bus', '')
            kabelvariante = json_data.get('kabelvariante', '')
            schnittstelle = ', '.join(json_data.get('schnittstelle', []))
            masse = ', '.join(json_data.get('masse', []))
            original_preis = float(match.group())
            reduzierter_preis = float(match.group())
            preisliste = get_preisliste(request)

            # Check if the item with matching values exists
            existing_item = InCartItem.objects.filter(
                benutzername=benutzername,
                akkuvariante=akkuvariante,
                mit_120_Ohm_CAN_Bus_Widerstand=CAN_Bus,
                kabelvariante=kabelvariante,
                schnittstelle=schnittstelle,
                masse=masse,
                original_preis=original_preis
            ).first()

            if existing_item:
                # Item already exists, update menge
                existing_item.menge += 1
                if existing_item.menge < 25:
                    existing_item.gesamt = existing_item.menge * existing_item.original_preis
                if existing_item.menge >= 25 and existing_item.menge < 50:
                    for preislist in preisliste:
                        if preislist['gehause'] == existing_item.akkuvariante and preislist['kabelvariante'] == existing_item.kabelvariante and float(preislist['qty_1']) == existing_item.original_preis:
                            existing_item.gesamt = existing_item.menge * float(preislist['qty_25'])
                            existing_item.reduzierter_preis = float(preislist['qty_25'])
                if existing_item.menge >= 50 and existing_item.menge < 100:
                    for preislist in preisliste:
                        if preislist['gehause'] == existing_item.akkuvariante and preislist['kabelvariante'] == existing_item.kabelvariante and float(preislist['qty_1']) == existing_item.original_preis:
                            existing_item.gesamt = existing_item.menge * float(preislist['qty_50'])  
                            existing_item.reduzierter_preis = float(preislist['qty_50'])
                if existing_item.menge >= 100 and existing_item.menge < 250:
                    for preislist in preisliste:
                        if preislist['gehause'] == existing_item.akkuvariante and preislist['kabelvariante'] == existing_item.kabelvariante and float(preislist['qty_1']) == existing_item.original_preis:
                            existing_item.gesamt = existing_item.menge * float(preislist['qty_100'])
                            existing_item.reduzierter_preis = float(preislist['qty_100']) 
                if existing_item.menge >= 250 and existing_item.menge < 500:
                    for preislist in preisliste:
                        if preislist['gehause'] == existing_item.akkuvariante and preislist['kabelvariante'] == existing_item.kabelvariante and float(preislist['qty_1']) == existing_item.original_preis:
                            existing_item.gesamt = existing_item.menge * float(preislist['qty_250'])
                            existing_item.reduzierter_preis = float(preislist['qty_250']) 
                if existing_item.menge >= 500 and existing_item.menge < 1000:
                    for preislist in preisliste:
                        if preislist['gehause'] == existing_item.akkuvariante and preislist['kabelvariante'] == existing_item.kabelvariante and float(preislist['qty_1']) == existing_item.original_preis:
                            existing_item.gesamt = existing_item.menge * float(preislist['qty_500']) 
                            existing_item.reduzierter_preis = float(preislist['qty_500'])
                if existing_item.menge >= 1000 and existing_item.menge < 2000:
                    for preislist in preisliste:
                        if preislist['gehause'] == existing_item.akkuvariante and preislist['kabelvariante'] == existing_item.kabelvariante and float(preislist['qty_1']) == existing_item.original_preis:
                            existing_item.gesamt = existing_item.menge * float(preislist['qty_1000'])
                            existing_item.reduzierter_preis = float(preislist['qty_1000'])
                if existing_item.menge >= 2000:
                    for preislist in preisliste:
                        if preislist['gehause'] == existing_item.akkuvariante and preislist['kabelvariante'] == existing_item.kabelvariante and float(preislist['qty_1']) == existing_item.original_preis:
                            existing_item.gesamt = existing_item.menge * float(preislist['qty_2000'])
                            existing_item.reduzierter_preis = float(preislist['qty_2000'])

                existing_item.save()
            else:
                # Item does not exist, create a new entry
                item_nummer = str(uuid.uuid4())
                InCartItem.objects.create(
                    item_nummer=item_nummer,
                    benutzername=benutzername,
                    akkuvariante=akkuvariante,
                    mit_120_Ohm_CAN_Bus_Widerstand=CAN_Bus,
                    kabelvariante=kabelvariante,
                    schnittstelle=schnittstelle,
                    masse=masse,
                    menge=1,
                    original_preis=original_preis,
                    reduzierter_preis=reduzierter_preis,
                    gesamt=original_preis
                )

            return JsonResponse({'success': True, 'message': 'Warenkorbartikel erfolgreich aktualisiert/erstellt.'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Fehler beim Aktualisieren/Erstellen des Warenkorbartikels: {str(e)}'})
    try:
        json_data = json.loads(request.body)
        json_string = json.dumps(json_data, ensure_ascii=False)
        match = re.search(r'\d+\.\d+', json_data['preis'])
        if not request.user.is_authenticated:
            login_url = reverse('login')  # Assuming you have a named URL pattern for the login page
            messages.warning(request, f'Um eine Bestellung aufzugeben, müssen Sie sich anmelden!')
            return JsonResponse({'message': 'You need to login to place an order', 'login_url': login_url})        
        else:
            benutzername = request.user.customerprofile.benutzername
            item_nummer = str(uuid.uuid4())
            akkuvariante = json_data.get('akkuvarianteName', '')
            CAN_Bus = json_data.get('CAN_Bus', '')
            kabelvariante = json_data.get('kabelvariante', '')
            schnittstelle = ', '.join(json_data.get('schnittstelle', []))
            masse = ', '.join(json_data.get('masse', []))
            original_preis = float(match.group())
            reduzierter_preis = float(match.group())
            
            inCartItems = InCartItem.objects.all()
            data = [{'item_nummer': inCartItem.item_nummer,
                'benutzername': inCartItem.benutzername,
                'akkuvariante': inCartItem.akkuvariante,
                'mit_120_Ohm_CAN_Bus_Widerstand':inCartItem.mit_120_Ohm_CAN_Bus_Widerstand,
                'kabelvariante': inCartItem.kabelvariante,
                'schnittstelle ': inCartItem.schnittstelle,
                'masse ': inCartItem.masse,
                'menge' : inCartItem.menge,
                'original_preis': inCartItem.original_preis,
                'reduzierter_preis': inCartItem.reduzierter_preis,
                'gesamt': inCartItem.gesamt} for inCartItem in inCartItems.filter(benutzername=benutzername)]
        
            cart_item = InCartItem.objects.create(
                item_nummer=item_nummer,
                benutzername=benutzername,
                akkuvariante=akkuvariante,
                mit_120_Ohm_CAN_Bus_Widerstand=CAN_Bus,
                kabelvariante=kabelvariante,
                schnittstelle=schnittstelle,
                masse=masse,
                menge=1,
                original_preis=original_preis,
                reduzierter_preis=reduzierter_preis,
                gesamt=original_preis
            )

            return JsonResponse({'success': True, 'message': 'Warenkorbartikel erfolgreich erstellt.'}, status=201)

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Fehler beim Erstellen des Warenkorbartikels: {str(e)}'})

@csrf_exempt
@require_POST
def upload_special_solution(request):
    ui_labels_data = get_ui_labels(request)
    try:
        print("request.user in upload_special_solution", request.user)
        if request.user.is_authenticated:
            order_nummer = str(uuid.uuid4())
            Ust_id = request.user.customerprofile.benutzername
            Status = 'Bestellt'
            hochgeladene_datei = request.FILES.get('specialfile')
            special_order = SpezielleBestellung(order_nummer=order_nummer, Ust_id=Ust_id, Status=Status, hochgeladene_datei=hochgeladene_datei)
            special_order.save()
            try:
                notificationService = NotificationService()
                notificationService.send_special_order_notification(request, special_order, ui_labels_data)
            except Exception as e:
                return JsonResponse({'message': 'Datei-Upload erfolgreich. Ihre Bestellung ist bei uns eingegangen und unsere Vertriebsmitarbeiter werden sich in Kürze mit Ihnen in Verbindung setzen', 'error': f'Error sending special order notification: {str(e)}'})
            messages.success(request, f'Datei-Upload erfolgreich. Ihre Bestellung ist bei uns eingegangen und unsere Vertriebsmitarbeiter werden sich in Kürze mit Ihnen in Verbindung setzen!')
            return JsonResponse({'message': 'Datei-Upload erfolgreich. Ihre Bestellung ist bei uns eingegangen und unsere Vertriebsmitarbeiter werden sich in Kürze mit Ihnen in Verbindung setzen'})
        else:
            login_url = reverse('login')  # Assuming you have a named URL pattern for the login page
            messages.warning(request, f'Um eine Bestellung aufzugeben, müssen Sie sich anmelden!')
            return JsonResponse({'message': 'You need to login to place an order', 'login_url': login_url})

    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'})