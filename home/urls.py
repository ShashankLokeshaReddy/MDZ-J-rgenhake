from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('accounts/register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('konfigurator/', views.konfigurator, name='konfigurator'),
    path('warenkorb/', views.warenkorb, name='warenkorb'),
    path('orders/', views.orders, name='orders'),
    path('profil/', views.profil, name='profil'),
    # path('customerProfile/', views.get_customer_profiles, name='get_customer_profiles'),
    # path('akkuvarianten/', views.get_akkuvarianten, name='get_akkuvarianten'),
    # path('kabelvarianten/', views.get_kabelvarianten, name='get_kabelvarianten'),
    # path('schnittstellen/', views.get_schnittstellen, name='get_schnittstellen'),
    # path('colors/', views.get_colors, name='get_colors'),
    # path('ui-labels/', views.get_ui_labels, name='get_ui_labels'),
    # path('images/', views.get_image_path, name='get_image_path'),
    path('developer_mode/', views.developer_mode, name='developer_mode'),
    path('update_colors/', views.update_colors, name='update_colors'),
    path('colors_url/', views.colors_url, name='colors_url'),
    path('cancel_order/', views.cancel_order, name='cancel_order'),
    path('order_again/', views.order_again, name='order_again'),
    path('delete_item/', views.delete_item, name='delete_item'),
    path('create_order_with_items/', views.create_order_with_items, name='create_order_with_items'),
    path('add_item_to_cart/', views.add_item_to_cart, name='add_item_to_cart'),
    path('upload_special_solution/', views.upload_special_solution, name='upload_special_solution'),
]
