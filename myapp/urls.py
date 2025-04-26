from django.urls import path
from . import views

urlpatterns = [
    path('',        views.home_view,        name='home'),
    path('about/',  views.about,            name='about'),
    path('contact/',views.contact,          name='contact'),
    path('menu/',   views.menu,             name='menu'),
    # path('login/', views.login_page, name='login'),
    # path('signup/', views.signup_page, name='signup'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
