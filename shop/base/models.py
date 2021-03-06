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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        ordering = ['-created_at']


User.customer = property(
    lambda u: Customer.objects.get_or_create(user=u, email=u.username)[0])


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
        Category, blank=False, null=True, on_delete=models.SET_NULL, related_name='products')
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(default='placeholder.jpg', blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    countInStock = models.IntegerField(default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    @property
    def get_avg_rating(self):
        reviews = Review.objects.filter(product=self)
        count = len(reviews)
        summary = 0
        try:
            for rvw in reviews:
                summary += rvw.rating
            return (int(summary/count))
        except ZeroDivisionError:
            return 0

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

    @property
    def is_available(self):
        if self.countInStock > 0:
            return True
        return False

    class Meta:
        ordering = ['-created_at']


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=False, null=True)
    rating = models.IntegerField(default=1)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return f'{self.rating}, {self.product.name}'


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name='orders')
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
    def get_cart_items(self):
        orderitems = self.orderitems.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return str(self.customer.name)

    class Meta:
        ordering = ['-date_ordered']


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

    class Meta:
        ordering = ['-date_added']


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, related_name='shipping_addresses')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=255, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.address)

    class Meta:
        ordering = ['-date_added']
