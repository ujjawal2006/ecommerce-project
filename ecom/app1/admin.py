from django.contrib import admin
from .models import Product, Profile, Cart ,Address

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'fname', 'lname', 'email', 'address', 'zip','pnumber')
    search_fields = ('fname', 'lname', 'email')
    list_filter = ('state',)

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    search_fields = ('user__username', 'product__name')
    list_filter = ('user', 'product')

class AddressAdmin(admin.ModelAdmin):
    list_display=('FullName','MobileNumber')    

admin.site.register(Product)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Cart, CartAdmin)  
admin.site.register(Address,AddressAdmin)
