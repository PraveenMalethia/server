from django.urls import path
from . import views

urlpatterns = [
  path('',views.index,name='index'),
  path('product/<str:uuid>/',views.productView,name='product-view'),
  path('add-to-cart/<str:uuid>/',views.addToCart,name='add-to-cart'),
  path('brands/',views.Brands,name='brands'),
  path('categories/',views.Categories,name='categories'),
]