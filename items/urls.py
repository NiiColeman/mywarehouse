from django.urls import path
from .views import (index, test_perm,
                    ItemUpdateView,
                    item_list,
                    item_detail_view,
                    expiring_list,
                    get_items,
                    delete_item,
                    search,
                    low_stock,
                    CategoryUpdateView,
                    CategoryCreateView,
                    delete_category,
                    category_detail,
                    cat_list,
                    )

app_name = 'items'

urlpatterns = [

    path('add', test_perm, name='add'),
    path('update/<int:pk>', ItemUpdateView.as_view(), name="item_update"),
    path('list', item_list, name='item_list'),
    path('expiring-list', expiring_list, name='expiring_list'),
    path('low-stock', low_stock, name='low_stock'),


    path("detail/<int:pk>/description", item_detail_view, name="item_detail"),
    path('<int:pk>/delete', delete_item, name='item_delete'),
    path("data", get_items, name="get-data"),
    path("search", search, name="search"),
    path("category/<int:pk>/update",
         CategoryUpdateView.as_view(), name="update_category"),
    path("category/create", CategoryCreateView.as_view(), name="category_create"),
    path("category/<int:pk>/delete", delete_category, name="category_delete"),
    path("category/list", cat_list, name="category_list"),
    path("category/<int:pk>/detail", category_detail, name="category_detail")


]
