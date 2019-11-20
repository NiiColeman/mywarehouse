"""warehouse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import ManagerSignUpView, user_list, UserCreateView, UserUpdateView, user_detail_view
from items.views import index
from .views import ItemChart, chartview, settings_view, settings_update_view
from carts.views import cart_home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/manager/',
         ManagerSignUpView.as_view(), name='manager_signup'),
    path('accounts/add/user/',
         UserCreateView.as_view(), name='add_user'),
    path('accounts/<int:pk>/update/user/',
         UserUpdateView.as_view(), name='update_user'),
    path('accounts/<int:pk>/details/user/',
         user_detail_view, name='user_detail'),



    path("accounts/users", user_list, name="users"),
    path("", index, name="index"),
    path("items/", include('items.urls')),
    path("orders/", include('orders.urls')),
    path("departments/", include("departments.urls")),
    path("api/chart/data/", ItemChart.as_view(), name="api-data"),
    path("chart/", chartview, name="chart"),
    path("cart", cart_home, name="cart"),
    path('settings', settings_view, name="settings"),
    path('settings/<int:pk>/update', settings_update_view, name="settings_update"),







]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
