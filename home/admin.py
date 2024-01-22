from django.contrib import admin
from .models import CustomerProfile, Akkuvariante, Kabelvariante, Schnittstelle, Color, UILabel, Image, InCartItem, Order, OrderItem

admin.site.register(CustomerProfile)
admin.site.register(Akkuvariante)
admin.site.register(Kabelvariante)
admin.site.register(Schnittstelle)
admin.site.register(Color)
admin.site.register(UILabel)
admin.site.register(Image)
admin.site.register(InCartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
