from django.urls import path
from django.views.generic.base import TemplateView
from .views import (OrderCreateView,
                    OrderListView,
                    order_list_view,
                    order_detail_view,
                    order_update_view,
                    delete_view,
                    search,
                    create_order,
                    list_order,
                    order_update,
                    order_delete
                    )


app_name = 'orders'

urlpatterns = [
    path("new-order", OrderCreateView.as_view(), name="new_order"),
    path("order-list", order_list_view, name="list_order"),
    path("<int:pk>/order-detail", order_detail_view, name="order_detail"),
    path("<int:pk>/order-update", order_update_view, name="order_update"),
    path("<int:pk>/order-delete", delete_view, name="order_delete"),
    path("search", search, name="search"),
    path("list",list_order,name="list_order"),
    path("create",create_order,name="create_order"),
    path('<int:pk>/update', order_update, name='order_updates'),
    path('<int:pk>/delete', order_delete, name='delete_order'),

    


    
]







