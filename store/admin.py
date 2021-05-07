from django.contrib import admin
from .models import Product , Category , Brand, Order, OrderItem, VillageOrCity, ShippingAddress
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(VillageOrCity)
admin.site.register(ShippingAddress)