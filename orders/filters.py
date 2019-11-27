import django_filters
from .models import Order


class OrderFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='icontains')
    year_of_order = django_filters.NumberFilter(
        field_name='date_of_order', lookup_expr='year')
    quantity__gt = django_filters.NumberFilter(
        field_name='quantity', lookup_expr='gt')
    quantity__lt = django_filters.NumberFilter(
        field_name='quantity', lookup_expr='lt')
    # expiry_month__lt = django_filters.NumberFilter(
    #     field_name='expiry_date', lookup_expr='month__lt')

    class Meta:
        model = Order
        fields = ['department','shelf', 'date_of_order', 'quantity']
