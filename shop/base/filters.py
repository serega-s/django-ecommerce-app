from django import forms
import django_filters
from django_filters.filters import CharFilter, RangeFilter

from .models import *

class ProductFilter(django_filters.FilterSet):
    price = RangeFilter(field_name='price')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    description = CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['id','image', 'slug', 'countInStock', 'created_at', 'price', 'name']