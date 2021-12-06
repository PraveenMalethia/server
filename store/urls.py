from django.urls import path
from . import views

urlpatterns = [
  path('',views.index,name='index'),
  path('product/<str:uuid>/',views.productView,name='product-view'),
  path('add-to-cart/',views.addToCart,name='add-to-cart'),
  path('remove-from-cart/<str:uuid>/',views.removeFromCart,name='remote-from-cart'),
  path('brands/',views.Brands,name='brands'),
  path('categories/',views.Categories,name='categories'),
  path('cart/',views.Cart,name='cart'),
  path('order/',views.OrderDetails,name='order'),
]