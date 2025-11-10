
from .models import Product , Profile , Cart ,Address
from django.shortcuts import render, get_object_or_404 , HttpResponse ,redirect
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


def home(request):
    return render (request , "home.html")

def Products(request):
    # Get all products from the Product model
    products = Product.objects.all()
    # Pass products to the template
    return render(request, 'products.html', {'products': products})

def product_detail(request, id):
    product = Product.objects.get(id=id)  # Get the product based on the ID
    return render(request, 'product_detail.html', {'product': product})

def signup(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')
        user = User.objects.create_user(username=username, password=password)
        user.save()
        login(request, user) 
        return redirect('profile')
    return render(request, 'signup.html')

def login_view(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")
    return render(request , 'login.html')

def logout_view(request):
    logout(request)  # This will log the user out
    return redirect('home')  # Redirect user to home page or any other page


def product_search(request):
    query = request.GET.get('q', '')  # Get the search query from the GET request
    products = Product.objects.filter(name__icontains=query)  # Case-insensitive search
    return render(request, 'product_search.html', {'products': products, 'query': query})

@login_required
def Create_account(request):
    if request.method == "POST":
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        pnumber = request.POST['number']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip']

        Profile.objects.create(
            user=request.user, 
            fname=fname,
            lname=lname,
            email=email,
            pnumber=pnumber,
            address=address,
            city=city,
            state=state,
            zip=zip_code
        )
        return redirect('home')
    return render(request, 'profile.html')

@login_required
def edt_profile(request):
    user = request.user
    try:
        data = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        data = None  
    return render(request, 'show_profile.html', {'data': data})




@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('show_cart')

@login_required
def show_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

def Delete_record(request ,id ):
    a=Cart.objects.get(pk=id)
    a.delete()
    return redirect("/")

@login_required
def deliveryaddres(request):
    if request.method == "POST":
        Address.objects.create(
        user=request.user,
        FullName = request.POST.get('name', ''),
        MobileNumber = request.POST.get('MobileNumber',''),
        Pincode = request.POST.get('pincode',''),
        Loclity = request.POST.get('locality', ''),
        Add = request.POST.get('address', ''),
        city = request.POST.get('city', ''),
        state = request.POST.get('state', ''),
        landamrk = request.POST.get('landmark', ''),
        APhone = request.POST.get('alt_phone', ''),
        )
        return redirect('deliveryaddres')  # redirect to same page after saving
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'deliveryaddres.html', {'addresses': addresses})


@login_required
def select_address_and_pay(request):
    if request.method == "POST":
        selected_id = request.POST.get('selected_address')
        if selected_id:
            request.session['selected_address_id'] = selected_id  # Save to session
            return redirect('Paymnet')
        else:
            messages.error(request, "Please select an address.")
            return redirect('deliveryaddres')


@login_required
def Paymnet(request):
    address_id = request.session.get('selected_address_id')
    selected_address = None
    if address_id:
        selected_address = Address.objects.filter(id=address_id, user=request.user).first()
    return render(request, 'payment.html', {'selected_address': selected_address})

import razorpay # type: ignore
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Use your test keys here
client = razorpay.Client(auth=("rzp_test_rfwWohDy6LXwEk", "QjcV15k4lUW2ppZFnoOFKhNg"))


@login_required
def Paymnet(request):
    address_id = request.session.get('selected_address_id')
    selected_address = None

    if address_id:
        selected_address = Address.objects.filter(id=address_id, user=request.user).first()

    # Generate Razorpay order here
    amount = 5000  # ₹50 in paise
    currency = 'INR'
    receipt = 'order_rcptid_11'

    razorpay_order = client.order.create({
        "amount": amount,
        "currency": currency,
        "receipt": receipt,
        "payment_capture": 1
    })

    context = {
        'selected_address': selected_address,
        'order_id': razorpay_order['id'],
        'amount': amount,
        'api_key': "rzp_test_rfwWohDy6LXwEk"
    }
    return render(request, 'payment.html', context)
@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        # You can get details from request.POST like:
        # razorpay_payment_id, razorpay_order_id, razorpay_signature
        print(request.POST)

        # (Optional) You can verify signature here using Razorpay SDK

    return render(request, 'success.html')
