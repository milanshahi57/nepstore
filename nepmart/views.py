from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Product, ContactMessage, UserProfile, Order, OrderItem

# Home Page
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def buy_now(request, product_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to continue shopping.")
        return redirect('login')
    
    # Get the product
    product = get_object_or_404(Product, id=product_id)
    
    # Add single product to cart
    cart = request.session.get('cart', {})
    cart[str(product_id)] = 1  # Set quantity to 1 for direct purchase
    request.session['cart'] = cart
    request.session.modified = True
    
    context = {
        'product': product,
        'total_price': product.price,  # Since quantity is 1
        'user': request.user,
    }
    
    return render(request, 'buy_now.html', context)

# Product List Page
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product.html', {'products': products})

# Product Detail Page
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

# Cart Page
@login_required(login_url='login')
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
@login_required(login_url='login')
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({
            "success": False,
            "message": "Please log in to add items to cart",
            "redirect": "/login/"
        }, status=403)

    if request.method == "POST":
        try:
            cart = request.session.get('cart', {})
            quantity = int(request.POST.get('quantity', 1))

            if str(product_id) in cart:
                cart[str(product_id)] += quantity
            else:
                cart[str(product_id)] = quantity

            request.session['cart'] = cart
            request.session.modified = True

            return JsonResponse({
                "success": True,
                "message": "Item added to the cart"
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": "Error adding item to cart"
            }, status=400)

    return JsonResponse({
        "success": False,
        "message": "Invalid request method"
    }, status=405)

# Update Cart Quantity
@login_required(login_url='login')
def update_cart(request, product_id):
    if request.method == "POST":
        new_quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})

        if new_quantity > 0:
            cart[str(product_id)] = new_quantity
        else:
            cart.pop(str(product_id), None)

        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart')

# Remove from Cart
@login_required(login_url='login')
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

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register_user')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register_user')

        # Create the User instance first
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,  # create_user will hash the password
            first_name=first_name,
            last_name=last_name
        )

        # UserProfile will be created automatically through the signal
        # But we can update it with additional fields if needed
        user.userprofile.phone = ''  # Add any additional fields here
        user.userprofile.save()

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')

    return render(request, 'register.html')

@login_required
def profile(request):
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)

    if request.method == 'POST':
        # Update user information
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        # Update profile information
        profile.phone = request.POST.get('phone', '')
        profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'profile.html', context)

@login_required
def orders(request):
    # Placeholder for orders view
    return render(request, 'orders.html')

@login_required
def order_detail(request, order_id):
    # Placeholder for order detail view
    return render(request, 'order_detail.html')

@login_required
def checkout(request):
    if request.method == 'POST':
        try:
            # Get cart items
            cart = request.session.get('cart', {})
            if not cart:
                messages.error(request, "Your cart is empty.")
                return redirect('cart')

            # Calculate total amount
            total_amount = 0
            order_items = []
            for product_id, quantity in cart.items():
                product = get_object_or_404(Product, id=int(product_id))
                total_amount += product.price * quantity
                order_items.append({
                    'product': product,
                    'quantity': quantity,
                    'price': product.price,
                    'total': product.price * quantity
                })

            # Create the order
            order = Order.objects.create(
                user=request.user,
                full_name=request.POST.get('full_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                address=request.POST.get('address_line1') + ' ' + request.POST.get('address_line2', ''),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                zip_code=request.POST.get('postal_code'),
                order_notes=request.POST.get('special_instructions', ''),
                total_amount=total_amount,
                status='pending',
                payment_method='cash_on_delivery'
            )

            # Create order items
            for item in order_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price'],
                    total=item['total']
                )

            # Clear the cart
            request.session['cart'] = {}
            request.session.modified = True

            messages.success(request, "Order placed successfully!")
            return redirect('order_confirmation', order_id=order.id)

        except Exception as e:
            print(f"Error creating order: {str(e)}")  # For debugging
            messages.error(request, "Order failed. Please try again.")
            return redirect('cart')

    return redirect('cart')

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_confirmation.html', {'order': order})
