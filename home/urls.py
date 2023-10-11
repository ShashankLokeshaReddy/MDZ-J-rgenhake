from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('purchase/', views.purchase, name='purchase'),
]
