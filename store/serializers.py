from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = OrderItem
        fields = '__all__'
    
    def get_product(self,obj):
        product = Product.objects.get(id=obj.product.id)
        serializer = ProductSerializer(product,many=False)
        return serializer.data

class OrderSerializer(serializers.ModelSerializer):
    cart_total = serializers.SerializerMethodField(read_only=True)
    cart_items = serializers.SerializerMethodField(read_only=True)
    orderItems = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'

    def get_cart_total(self,obj):
        orderitems = obj.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    def get_cart_items(self,obj):
        return obj.orderitem_set.count()

    def get_orderItems(self,obj):
        orderitems = obj.orderitem_set.all()
        serializers = OrderItemSerializer(orderitems,many=True)
        return serializers.data

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'
        exclude = ['customer','order']

class CustomUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['password']