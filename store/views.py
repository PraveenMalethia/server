from django.shortcuts import render
from .models import Product , Brand , Category
from django.db.models import Q

# rest framework class based view mixing 
from rest_framework.views import APIView

# rest framework function based view mixing 
from .serializers import (ProductSerializer,
    BrandSerializer,
    CategorySerializer
    )
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser
# Create your views here.

@api_view(['GET'])
def index(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def productView(request,uuid):
    try:
        product = Product.objects.get(id=uuid)
        serializer = ProductSerializer(product,many=False)
        return Response(serializer.data)
    except:
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