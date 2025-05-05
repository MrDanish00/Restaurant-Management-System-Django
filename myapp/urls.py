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
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    path('accounts/login/', views.login_view, name='login'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),
]




