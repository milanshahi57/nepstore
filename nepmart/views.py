from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Product

# Home Page
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def buy_now(request):
    return render(request, 'buy_now.html')

# Product List Page
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product.html', {'products': products})

# Product Detail Page
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

# Cart Page
def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': product.price * quantity
        })
        total_price += product.price * quantity

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

# Add to Cart without Redirection
def add_to_cart(request, product_id):
    if request.method == "POST":
        cart = request.session.get('cart', {})

        quantity = int(request.POST.get('quantity', 1))  # Get quantity from form

        if str(product_id) in cart:
            cart[str(product_id)] += quantity
        else:
            cart[str(product_id)] = quantity

        request.session['cart'] = cart
        request.session.modified = True

        # Return JSON response instead of redirecting
        return JsonResponse({"success": True, "message": "Item added to the cart"})

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

# Update Cart Quantity
def update_cart(request, product_id):
    if request.method == "POST":
        new_quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})

        if new_quantity > 0:
            cart[str(product_id)] = new_quantity
        else:
            cart.pop(str(product_id), None)  # Remove if quantity is zero

        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart')

# Remove from Cart
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

def contact(request):
    return render(request, 'contact.html')

# Contact Form Submission
from .models import ContactMessage
from django.contrib import messages

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, message=message)
            messages.success(request, "Your message has been sent successfully!")
        else:
            messages.error(request, "Please fill in all fields before submitting.")

        return redirect("contact")  

    return render(request, "contact.html")

# Login
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home or dashboard
        else:
            messages.error(request, "Invalid username or password!")  
            return redirect('login')

    return render(request, 'login.html')

# Register User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.hashers import make_password, check_password

def register_user(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register_user')

        if UserProfile.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register_user')

        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register_user')

        hashed_password = make_password(password)
        new_user = UserProfile(first_name=first_name, last_name=last_name, email=email, username=username, password=hashed_password)
        new_user.save()

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')

    return render(request, 'register.html')
