from django.shortcuts import HttpResponse, render

from .models import Category, Product
from .utils import cartData


def home(request):
    products = Product.objects.all()
    category = request.GET.get('category')

    if category == None:
        products = Product.objects.all().order_by('-created_at')
    else:
        products = Product.objects.filter(
            category__name=category).order_by('-created_at')
    context = {
        'products': products,
    }

    return render(request, 'base/home.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems
    }

    return render(request, 'base/cart.html', context)


def product(request, category_slug, product_slug):
    product = Product.objects.get(
        category__slug=category_slug, slug=product_slug)
    related_products = list(
        product.category.product_set.exclude(id=product.id))

    context = {
        'product': product,
        'related_products': related_products
    }

    return render(request, 'base/product.html', context)


def register(request):

    context = {}

    return render(request, 'base/register.html', context)


def login(request):

    context = {}

    return render(request, 'base/login.html', context)


def checkout(request):

    context = {}

    return render(request, 'base/checkout.html', context)
