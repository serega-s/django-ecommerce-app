from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name="cart"),
    path('product/<slug:category_slug>/<slug:product_slug>/',
         views.product, name='product'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.profile, name='profile'),

    path('register/', views.register_customer, name='register_customer'),
    path('login/', views.login_customer, name='login_customer'),
    path('logout/', views.logout_customer, name='logout_customer'),
    path('edit_customer/', views.edit_customer, name="edit_customer"),

    path('update_item/', views.update_item),
    path('process_order/', views.process_order),
    path('add_comment/', views.add_comment),
]
