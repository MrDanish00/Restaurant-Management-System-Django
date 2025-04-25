from django.urls import path
from . import views
from .views import login_signup_view

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('',        views.home_view,        name='home'),
    path('about/',  views.about,            name='about'),
    path('contact/',views.contact,          name='contact'),
    path('services/',views.services,        name='services'),
    path('menu/',   views.menu,             name='menu'),
    path('auth/', views.login_signup_view,        name='login_signup'),
    path('logout/', views.logout_view,      name='logout'),
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup')
]
