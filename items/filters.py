import django_filters
from .models import Category, Item, User


class ItemFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    expiry_year = django_filters.NumberFilter(
        field_name='expiry_date', lookup_expr='year')
    expiry_month__gt = django_filters.NumberFilter(
        field_name='expiry_date', lookup_expr='month__gt')
    expiry_month__lt = django_filters.NumberFilter(
        field_name='expiry_date', lookup_expr='month__lt')

    class Meta:
        model = Item
        fields = ['user', 'name', 'category', 'stock_on_hand',
                  'expiry_date', 'shelf_number', 'perishable', 'timestamp']


# class OrderFilter(django_filters.FilterSet):
