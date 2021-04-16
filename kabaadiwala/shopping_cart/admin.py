from django.contrib import admin

from .models import OrderItem, Order,ShippingAddress

admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(ShippingAddress)