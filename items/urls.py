from django.urls import path
from .views import (index, test_perm,
 ItemUpdateView, 
 item_list, 
 item_detail_view, 
 expiring_list, 
 get_items,
 delete_item,
 search)

app_name = 'items'

urlpatterns = [

    path('add', test_perm, name='add'),
    path('update/<int:pk>', ItemUpdateView.as_view(), name="item_update"),
    path('list', item_list, name='item_list'),
    path('expiring-list', expiring_list, name='expiring_list'),

    path("detail/<int:pk>/description", item_detail_view, name="item_detail"),
    path('<int:pk>/delete', delete_item, name='item_delete'),
    path("data", get_items, name="get-data"),
    path("search", search, name="search")
]
