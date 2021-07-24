from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name="cart"),
    path('product/<slug:category_slug>/<slug:product_slug>/', views.product, name='product'),
]
