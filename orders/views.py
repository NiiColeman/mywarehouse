from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
# Create your views here.
from .models import Order
from .forms import OrderForm
from items.models import Item
from departments.models import Department

import uuid


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = "orders/new_order.html"

    def form_valid(self, form):

        item = Item.objects.get(name=form.instance.item)
        item.stock_on_hand = item.stock_on_hand-form.instance.quantity
        order_id = generate_random_string(item.name)
        form.instance.order_id = order_id
        item.save()
        form.save()
        return redirect("orders:list_order")


class OrderListView(ListView):
    model = Order
    template_name = "orders/order_list.html"


def order_list_view(request):
    orders = Order.objects.all()
    items = Item.objects.all()
    departments = Department.objects.all()

    context = {
        'items': items,
        'departments': departments,
        'orders':orders,
    }

    return render(request, 'orders/order_list.html', context)


def generate_random_string(item):
    item_name = item.replace(' ', '-')
    rand_code = my_uuid = uuid.uuid4()
    return "{}-{}".format(item_name, rand_code)
