import django_filters
from .models import Order





class OrderFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='icontains')
    # expiry_year = django_filters.NumberFilter(
    #     field_name='expiry_date', lookup_expr='year')
    # expiry_month__gt = django_filters.NumberFilter(
    #     field_name='expiry_date', lookup_expr='month__gt')
    # expiry_month__lt = django_filters.NumberFilter(
    #     field_name='expiry_date', lookup_expr='month__lt')

    class Meta:
        model = Item
        fields = ['department','item','date_of_order',]



class OrderFilter(django_filters.FilterSet):
    