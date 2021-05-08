from rest_framework import serializers
from .models import *

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
    order_product = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['quantity','order_product']

    def get_order_product(self, product):
        serializer = ProductSerializer(product, many=False)
        return serializer.data