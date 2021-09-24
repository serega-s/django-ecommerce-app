import json

from .models import Customer, Order, OrderItem, Product


def cookieCart(request):
    items = []

    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('Cart', cart)

    order = {'get_cart_items': 0, 'get_cart_total': 0}

    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'category': product.category,
                    'image': product.image,
                    'slug': product.slug
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }

            items.append(item)
        except:
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitems.all()
        cartItems = order.get_cart_items#get_items_total 

    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}

def guestOrder(request, data):
    print('User is not  logged in!')

    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    print('NAME:', name, 'EMAIL:', email)

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email
    )

    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )

        product.countInStock -= item['quantity']
        if product.countInStock <= 0:
            product.countInStock = 0

        product.save()
    return customer, order


