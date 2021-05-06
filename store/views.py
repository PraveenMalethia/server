from django.shortcuts import render
from .models import Product
from django.db.models import Q

# rest framework class based view mixing 
from rest_framework.views import APIView

# rest framework function based view mixing 
from .serializers import ProductSerializer
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
