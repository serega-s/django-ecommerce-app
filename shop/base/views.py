import datetime
import json
from .filters import ProductFilter

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import logout_then_login
from django.http.response import JsonResponse
from django.shortcuts import redirect, render

from .forms import EditCustomerForm, UserCreateForm, UserLoginForm
from .models import (Customer, Order, OrderItem, Product, Review,
                     ShippingAddress)
from .utils import cartData, guestOrder


def home(request):
    products = Product.objects.all()
    my_filter = ProductFilter(request.GET, queryset=products)

    products = my_filter.qs
    
    context = {
        'products': products,
        'my_filter': my_filter
    }

    return render(request, 'base/home.html', context)


def cart(request):
    data = cartData(request)

    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
    }

    return render(request, 'base/cart.html', context)


def product(request, category_slug, product_slug):
    product = Product.objects.get(
        category__slug=category_slug, slug=product_slug)
    related_products = list(
        product.category.products.exclude(id=product.id))
    reviews = product.reviews.all().order_by('-created_at')
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews
    }

    return render(request, 'base/product.html', context)


def register_customer(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            customer = Customer.objects.create(
                name=user.first_name, email=user.username, user=request.user)

            return redirect('home')
    else:
        form = UserCreateForm()

    context = {
        'form': form,
    }

    return render(request, 'base/register.html', context)


def login_customer(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd['username'], password=cd['password'])

            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserLoginForm()

    context = {
        'form': form
    }

    return render(request, 'base/login.html', context)

@login_required
def edit_customer(request):
    customer = request.user.customer

    if request.method == "POST":
        form = EditCustomerForm(request.POST, instance=customer)

        if form.is_valid():
        
            username = form.cleaned_data['email']
            full_name = form.cleaned_data['name']


            customer.user.username = username
            customer.user.save()

            customer.email = username
            customer.save()

            customer.name = full_name
            customer.save()

            return redirect('profile')
    else:
        form = EditCustomerForm(instance=customer)

    context = {
        'customer': customer,
        'form': form
    }
    
    return render(request, 'base/edit_customer.html', context)

def checkout(request):
    data = cartData(request)

    order = data['order']
    items = data['items']

    context = {
        'order': order,
        'items': items,
    }

    return render(request, 'base/checkout.html', context)


@login_required
def logout_customer(request):
    logout_then_login(request)

    return redirect('login_customer')

@login_required
def profile(request):
    customer = request.user.customer
    orders = customer.orders.filter(complete=True)

    context = {
        'customer': customer,
        'orders': orders
    }
    
    return render(request, 'base/profile.html', context)


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    quantity = data['quantity']

    print(data)

    print(f'productId: {productId}, action: {action}')

    customer = request.user.customer
    
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity += int(quantity)
        product.countInStock -= orderItem.quantity - 1
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        product.countInStock += orderItem.quantity + 1

    product.countInStock -= orderItem.quantity
    if product.countInStock <= 0:
        product.countInStock = 0

    product.save()
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def process_order(request):
    print('DATA:', request.body)
    data = json.loads(request.body)

    transaction_id = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False
        )
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        postal_code=data['shipping']['postal_code'],
        country=data['shipping']['country']
    )

    return JsonResponse('Payment submitted...', safe=False)


def add_comment(request): 
    data = json.loads(request.body)
    print('DATA:', data)

    Review.objects.create(
        product_id=data['data']['product'],
        customer=request.user.customer,
        rating=int(data['data']['rating']),
        comment=data['data']['comment']
    )

    return JsonResponse('Comment was added',safe=False)