from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('purchase/', views.purchase, name='purchase'),
    path('customerProfile/', views.get_customer_profiles, name='get_customer_profiles'),
    path('akkuvarianten/', views.get_akkuvarianten, name='get_akkuvarianten'),
    path('kabelvarianten/', views.get_kabelvarianten, name='get_kabelvarianten'),
    path('schnittstellen/', views.get_schnittstellen, name='get_schnittstellen'),
    path('colors/', views.get_colors, name='get_colors'),
    path('ui-labels/', views.get_ui_labels, name='get_ui_labels'),
    path('images/', views.get_image_path, name='get_image_path'),
]
