from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from decimal import Decimal
from app1.models import Product, Profile, Cart
from .forms import ProductForm

def staff_check(user):
    return user.is_authenticated and user.is_staff

# ---------- Dashboard ----------
@user_passes_test(staff_check, login_url='login')
def dashboard(request):
    total_products = Product.objects.count()
    total_customers = Profile.objects.count()

    total_sales = Cart.objects.aggregate(
        total=Sum(
            ExpressionWrapper(F('product__price') * F('quantity'),
                              output_field=DecimalField(max_digits=12, decimal_places=2))
        )
    )['total'] or Decimal('0.00')

    # Top 5 products by quantity
    top = (Cart.objects
             .values('product__name')
             .annotate(qty=Sum('quantity'))
             .order_by('-qty')[:5])
    labels = [row['product__name'] for row in top]
    data   = [row['qty'] for row in top]

    return render(request, 'manager/dashboard.html', {
        'total_products': total_products,
        'total_customers': total_customers,
        'total_sales': total_sales,
        'chart_labels': labels,
        'chart_data': data,
    })

# ---------- Products ----------
# @user_passes_test(staff_check, login_url='login')
def product_list(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'manager/product_list.html', {'products': products})

# @user_passes_test(staff_check, login_url='login')
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('admin_products')
    else:
        form = ProductForm()
    return render(request, 'manager/product_form.html', {'form': form, 'title': 'Add Product'})

# @user_passes_test(staff_check, login_url='login')
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('admin_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'manager/product_form.html', {'form': form, 'title': 'Edit Product'})

# @user_passes_test(staff_check, login_url='login')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'Product deleted.')
    return redirect('admin_products')

# ---------- Customers ----------
# @user_passes_test(staff_check, login_url='login')
def profile_list(request):
    profiles = Profile.objects.select_related('user').order_by('-id')
    return render(request, 'manager/profile_list.html', {'profiles': profiles})
