from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('purchase/', views.purchase, name='purchase'),
    path('profile/', views.profile, name='profile'),
    # path('customerProfile/', views.get_customer_profiles, name='get_customer_profiles'),
    # path('akkuvarianten/', views.get_akkuvarianten, name='get_akkuvarianten'),
    # path('kabelvarianten/', views.get_kabelvarianten, name='get_kabelvarianten'),
    # path('schnittstellen/', views.get_schnittstellen, name='get_schnittstellen'),
    # path('colors/', views.get_colors, name='get_colors'),
    # path('ui-labels/', views.get_ui_labels, name='get_ui_labels'),
    # path('images/', views.get_image_path, name='get_image_path'),
    # path('orders/', views.get_image_path, name='get_orders'),
    path('developer_mode/', views.developer_mode, name='developer_mode'),
    path('update_colors/', views.update_colors, name='update_colors'),
    path('colors_url/', views.colors_url, name='colors_url'),
]
