from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),
    path('products/', views.product_list, name='admin_products'),
    path('products/new/', views.product_create, name='admin_product_create'),
    path('products/<int:pk>/edit/', views.product_edit, name='admin_product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='admin_product_delete'),

    path('customers/', views.profile_list, name='admin_customers'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
