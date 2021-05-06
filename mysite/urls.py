from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls'),name="store"),
    path('api/auth/', include('dj_rest_auth.urls'),name="users"),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls'),name="registrations"),
    path('api/auth/facebook/', views.FacebookLogin.as_view(), name='fb_login'),
]
