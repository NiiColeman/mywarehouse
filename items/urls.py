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
                    item_page,
                    post_item,
                    add_to_shelf,
                    shelf_list, shelf_detail, update_shelf, delete_shelf, upload_excel


                    )

app_name = 'items'

urlpatterns = [

    path('add', test_perm, name='add'),
    path('add-item', item_page, name='add-item'),
    path('post-item', post_item, name="post-item"),
    path('upload-items', upload_excel, name="upload_items"),
    path("shelf/add-to-shelf", add_to_shelf, name="add_shelf"),
    path("shelf/list", shelf_list, name="shelf_list"),
    path("shelf/<int:pk>/detail", shelf_detail, name="shelf_detail"),
    path("shelf/<int:pk>/update", update_shelf, name="shelf_update"),
    path("shelf/<int:pk>/delete", delete_shelf, name="shelf_delete"),








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
    path("category/<int:pk>/detail", category_detail, name="category_detail"),
    # path('item-update/<int:pk>', items_update, name="update"),



]
