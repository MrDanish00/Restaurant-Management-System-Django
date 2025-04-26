from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def home_view(request):
    return render(request, 'index.html')  

def contact(request):
    return render(request, 'contact.html')

def menu(request):
    return render(request, 'menu.html')

def signup_page(request):
    return render(request, 'signup.html')

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
                return redirect('home')  # ✅ Redirect to home page

            else:
                messages.error(request, 'Invalid email or password.')  # ❌ RED message
        except User.DoesNotExist:
            messages.error(request, 'No user with that email.')  # ❌ RED message

    return render(request, 'login.html')

def logout_view(request):
    # Only accept POST for logout (more secure than GET)
    if request.method == 'POST':
        logout(request)  
        messages.success(request, "You’ve been logged out successfully.")
        return redirect('home')  # or wherever you want
    # If someone GETs this URL, just send them home (or login)
    return redirect('home')