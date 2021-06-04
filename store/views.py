from .models import Product , Brand , Category , Order , OrderItem
from django.db.models import Q , Count
from django.contrib.auth.models import User


# rest framework function based view mixing 
from .serializers import (
    ProductSerializer,
    BrandSerializer,
    CategorySerializer,
    OrderItemSerializer,
    ShippingAddressSerializer)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# Create your views here.

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def index(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def productView(request,uuid):
    try:
        product = Product.objects.get(id=uuid)
        recommendation = Product.objects.filter(category=product.category.id).annotate(sales_count=Count('sales')).exclude(id=product.id).order_by('sales_count')
        serializer = ProductSerializer(product,many=False)
        RSerializers = ProductSerializer(recommendation,many=True)
        return Response({'product':serializer.data,'recommendations':RSerializers.data})
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def addToCart(request,uuid):
    try:
        # user = request.user
        user = User.objects.get(username='admin')
        product = Product.objects.get(id=uuid)
        order , created = Order.objects.get_or_create(customer=user,placed=False)
        try:
            orderItem = OrderItem.objects.get(product=product, order=order)
            if orderItem is not None:
                orderItem.quantity += 1
                orderItem.save()
        except OrderItem.DoesNotExist:
            orderItem = OrderItem.objects.create(product=product, order=order, quantity=1)
            orderItem.save()
        serializer = ProductSerializer(product,many=False)
        return Response(serializer.data)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def removeFromCart(request,uuid):
    try:
        # user = request.user
        user = User.objects.get(username='admin')
        product = Product.objects.get(id=uuid)
        order = Order.objects.get(customer=user,placed=False)
        try:
            orderItem = OrderItem.objects.get(product=product, order=order)
            if orderItem.quantity == 1:
                orderItem.delete()
            else:
                orderItem.quantity -= 1
                orderItem.save()
        except OrderItem.DoesNotExist:
            pass
        serializer = ProductSerializer(product,many=False)
        return Response(serializer.data)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def Brands(request):
    brands = Brand.objects.all()
    serializer = BrandSerializer(brands,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def Categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def Cart(request):
    # user = request.user
    user = User.objects.get(username='admin')
    order = Order.objects.get(customer=user,placed=False)
    orderItems = order.orderItems
    serializer = OrderItemSerializer(orderItems,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def Checkout(request):
    # user = request.user
    user = User.objects.get(username='admin')
    order = Order.objects.get(customer=user,placed=False)
    serializer = ShippingAddressSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)
    return Response(serializer.data,status=status.HTTP_200_OK)