from django.urls import path
from .views import OrderCreateView, OrderListView, order_list_view, order_detail_view, order_update_view, delete_view


app_name = 'orders'

urlpatterns = [
    path("new-order", OrderCreateView.as_view(), name="new_order"),
    path("order-list", order_list_view, name="list_order"),
    path("<int:pk>/order-detail", order_detail_view, name="order_detail"),
    path("<int:pk>/order-update", order_update_view, name="order_update"),
    path("<int:pk>/order-delete", delete_view, name="order_delete"),


]
