import json
from .models import Product

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
                    'image': product.image
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
        pass

    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}