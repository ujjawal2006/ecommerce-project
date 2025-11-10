"""
URL configuration for ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from app1 import views 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('products/', views.Products, name='Products'),  # URL pattern for the products page
    path('product/<int:id>/', views.product_detail, name='product_detail'),  # URL for product details
    path('signup/',views.signup, name='signup'),
    path('login/',views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
   
    path('profile/' , views.Create_account , name='profile'),
    path('profile/' , views.Create_account , name='profile'),
    path('search/', views.product_search, name='product_search'),
    path('show_profile/', views.edt_profile, name="edt_profile"), 
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.show_cart, name='show_cart'),
    path('delete_record',views.Delete_record,name="delete"),
    path('Enteraddres', views.deliveryaddres , name="deliveryaddres"),
    path('Payment',views.Paymnet, name="Paymnet"),
    path('select_address/', views.select_address_and_pay, name='select_address_and_pay'),
    path('payment-success/', views.payment_success, name='payment-success'),

    # custome admin
    path('admin/', admin.site.urls),  # default django admin
    path('manage/', include('manager.urls')),


#      path('accounts/', include('django.contrib.auth.urls')),  # ✅ login system

   







]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
