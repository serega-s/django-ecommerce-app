import json

from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from django.shortcuts import HttpResponse, render

from .models import Category, Order, OrderItem, Product
from .utils import cartData


def home(request):
    products = Product.objects.all()
    category = request.GET.get('category')
    query = request.GET.get('query')
    if category == None:
        products = Product.objects.all().order_by('-created_at')
    else:
        products = Product.objects.filter(
            category__name=category).order_by('-created_at')

    if query == None:
        products = Product.objects.all().order_by('-created_at')
    else:
        products = Product.objects.filter(
            Q(category__name__icontains=query) | Q(name__icontains=query) | Q(description__icontains=query)).order_by('-created_at')

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


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print(f'productId: {productId}, action: {action}')

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete

    return JsonResponse('Item was added', safe=False)
