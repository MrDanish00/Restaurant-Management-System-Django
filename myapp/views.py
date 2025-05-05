from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout 
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from .models import Product, OrderItem, Order
from django.template.loader import render_to_string
from django.db import transaction
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def home_view(request):
    return render(request, 'index.html')  

def contact(request):
    return render(request, 'contact.html')

def menu(request):
    foods = Product.objects.all()
    food_images = foods
    return render(request, 'menu.html', {'food_images': food_images})


def signup_page(request):
    return render(request, 'signup.html')
def order_confirmation(request):
    return render(request, 'order_confirmation.html')


def login_page(request):
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Account created successfully!')
                return redirect('login')
            except IntegrityError:
                messages.error(request, "Username already taken. Please choose a different username")
        else:
            messages.error(request, 'Signup failed. Please check the errors.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully logged in!')
                return redirect('home') 

            else:
                messages.error(request, 'Invalid email or password.')  
        except User.DoesNotExist:
            messages.error(request, 'No user with that email.')  

    return render(request, 'login.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)  
        messages.success(request, "You’ve been logged out successfully.")
        return redirect('home')  
    return redirect('home')


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from django.views.decorators.http import require_POST
from django.middleware.csrf import get_token

from django.contrib.auth.decorators import login_required




from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        cart_item, created = OrderItem.objects.get_or_create(
            user=request.user,
            product=product,
            ordered=False
        )
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        messages.success(request, f"{product.name} has been added to the cart.")
        return redirect('menu')




@login_required
def cart(request):
    cart_items = OrderItem.objects.filter(user=request.user, ordered=False)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_amount': total_amount,
    })



@login_required
def remove_from_cart(request, product_id):
    item = get_object_or_404(OrderItem, id=product_id, user=request.user, ordered=False)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart')


@login_required
def checkout(request):
    cart_items = OrderItem.objects.filter(user=request.user, ordered=False)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            ordered=True
        )
        order.items.set(cart_items)
        cart_items.update(ordered=True)

        messages.success(request, "Order placed successfully!")
        return redirect('order_confirmation')

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_amount': total_amount,
    })


@login_required
def order_confirmation(request):
    latest_order = Order.objects.filter(user=request.user).order_by('-ordered_date').first()
    return render(request, 'order_confirmation.html', {
        'order': latest_order,
        'cart_items': latest_order.items.all(),
        'total_amount': latest_order.amount_to_pay,
    })



@login_required
def place_order(request):
    if request.method == "POST":
        # Collect form data
        name           = request.POST.get('name')
        phone          = request.POST.get('phone')
        address        = request.POST.get('address')
        payment_method = request.POST.get('payment_method')
        
        # Grab all un–ordered items in the cart
        cart_items = OrderItem.objects.filter(user=request.user, ordered=False)

        # Calculate total
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        
        # Wrap in a transaction so stock and order placement stay in sync
        with transaction.atomic():
            # Create the order
            order = Order.objects.create(
                user=request.user,
                name=name,
                phone=phone,
                address=address,
                payment_method=payment_method,
                amount_to_pay=total_amount,
                ordered=True
            )
            order.items.set(cart_items)

            # Decrease stock for each product
            for item in cart_items:
                product = item.product
                if product.quantity < item.quantity:
                    # Not enough stock: roll back
                    raise ValueError(f"Not enough stock for {product.name}")
                product.quantity -= item.quantity
                product.save()

            # Mark those items as ordered
            cart_items.update(ordered=True)

        messages.success(request, "Your order has been placed successfully!")
        return render(request, 'order_confirmation.html', {
            'cart_items': cart_items,
            'total_amount': total_amount,
            'name': name,
            'address': address,
            'phone': phone,
            'payment_method': payment_method
        })

    return redirect('cart')