import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

'''
1.Registration (email, name & password) - Selecting some product - Adding to Cart - Checkout - Order(no email & name)
2. No registration - Selecting some product - Adding to Cart - Checkout - Order(email & name)
'''


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = None
        if self.slug == None:
            slug = slugify(self.name)

            has_slug = Category.objects.filter(slug=slug).exists()
            count = 1

            while has_slug:
                count += 1
                slug = slugify(self.name) + '-' + str(count)
                has_slug = Category.objects.filter(slug=slug).exists()

            self.slug = slug
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(
        Category, blank=False, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(default='placeholder.jpg', blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    slug = models.SlugField(blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    countInStock = models.IntegerField(default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = None
        if self.slug == None:
            slug = slugify(self.name)

            has_slug = Category.objects.filter(slug=slug).exists()
            count = 1

            while has_slug:
                count += 1
                slug = slugify(self.name) + '-' + str(count)
                has_slug = Category.objects.filter(slug=slug).exists()

            self.slug = slug
        super().save(*args, **kwargs)


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=255, blank=False, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    @property
    def get_cart_total(self):
        orderitems = self.orderitems.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_items_total(self):
        orderitems = self.orderitems.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return self.customer.name


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return self.product.name


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=255, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.address)
