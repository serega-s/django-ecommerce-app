from .models import Category
from .utils import cartData

def menu_categories(request):
    categories = Category.objects.all()

    return {'menu_categories': categories}


def cart_items(request):

    data = cartData(request)

    cartItems = data['cartItems']
    return {'cartItems': cartItems}