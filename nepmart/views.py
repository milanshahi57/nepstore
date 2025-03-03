from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

# Home Page
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html',  {'products': products})

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

# Add to Cart with Quantity
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))  # Get quantity from form
    else:
        quantity = 1  # Default to 1 if no quantity is provided

    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

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


# for contact form submission
from .models import ContactMessage
from django.contrib import messages



def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if name and email and message:
            # Save to database
            ContactMessage.objects.create(name=name, email=email, message=message)

            # Success message
            messages.success(request, "Your message has been sent successfully!")
        else:
            # Error message
            messages.error(request, "Please fill in all fields before submitting.")

        return redirect("contact")  # Redirect to clear form and display message

    return render(request, "contact.html")

def login(request):
    return render(request, 'login.html')

# register the User 
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login

def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        user = User.objects.create_user(
            first_name=first_name, last_name=last_name, 
            username=username, email=email, password=password
        )
        user.save()
        messages.success(request, "Registration successful!")
        return redirect("register")  # Redirect back to register page to show message

    return render(request, "register.html")
