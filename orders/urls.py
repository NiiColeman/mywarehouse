from django.urls import path
from .views import OrderCreateView, OrderListView,order_list_view


app_name = 'orders'

urlpatterns = [
    path("new-order", OrderCreateView.as_view(), name="new_order"),
    path("order-list", order_list_view, name="list_order"),
]
