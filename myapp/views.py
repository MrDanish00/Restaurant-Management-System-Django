from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def home_view(request):
    return render(request, 'index.html')  

def contact(request):
    return render(request, 'contact.html')

def services(request):
    return render(request, 'service.html')

def menu(request):
    return render(request, 'menu.html')
def signup_page(request):
    return render(request, 'signup.html')


def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

def login_signup_view(request):
    signup_form = CustomUserCreationForm()
    login_form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if 'signup' in request.POST:
            signup_form = CustomUserCreationForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                return redirect('home')

        elif 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('home')

    return render(request, 'login_signup.html', {
        'signup_form': signup_form,
        'login_form': login_form,
    })
