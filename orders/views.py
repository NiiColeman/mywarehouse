from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView
# Create your views here.
from .models import Order
from .forms import OrderForm
from items.models import Item
from departments.models import Department
from django.contrib import messages
from invoices.models import Invoice
import uuid


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = "orders/new_order.html"

    def form_valid(self, form):

        item = Item.objects.get(name=form.instance.item)
        item.stock_on_hand = item.stock_on_hand-form.instance.quantity

        if item.stock_on_hand < form.instance.quantity:

            messages.success(
                self.request, 'Order cannot be placed, requested itemsare more than the items in your inventory')
            return redirect('orders:list_order')

        elif item.stock_on_hand < 1:
            messages.success(self.request, 'Item is low on stock')
            return redirect('orders:list_order')

        else:
            order_id = generate_random_string(item.name)
            form.instance.order_id = order_id
            item.save()
            form.save()
            order=get_order(order_id=order_id)
            invoice_id=invoice_id=generate_invoice_id()
            create_invoice(order,invoice_id)
            messages.success(
                self.request, 'Order Has Been Made')
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
        'orders': orders,
    }

    return render(request, 'orders/order_list.html', context)


def generate_random_string(item):
    item_name = item.replace(' ', '-')
    rand_code = my_uuid = uuid.uuid4()
    return "{}-{}".format(item_name, rand_code)


# display the details of the order
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form=OrderForm(request.POST or None, instance=order)

    context = {
        'order': order,
        'form':form
    }

    return render(request, 'orders/order_detail.html', context)


def order_update_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    new_order = get_order(order.order_id)
    # print(new_order.quantity)

    form = OrderForm(request.POST or None, instance=order)

    if request.method == "POST":

        form = OrderForm(request.POST or None, instance=order)

        if form.is_valid():
            item = Item.objects.get(name=form.instance.item)

            if item.stock_on_hand < form.instance.quantity:

                messages.success(
                    request, 'Order cannot be placed, requested itemsare more than the items in your inventory')
                return redirect('orders:list_order')

            elif item.stock_on_hand < 1:
                messages.success(request, 'Item is low on stock')
                return redirect('orders:list_order')

            else:
                old_order = get_order(order.order_id)

                if form.instance.quantity < old_order.quantity:
                    newq = old_order.quantity-form.instance.quantity
                    print('item stock on hand : {}'.format(item.stock_on_hand))
                    item.stock_on_hand = item.stock_on_hand + newq
                    print('item stock on hand : {}'.format(item.stock_on_hand))

                    item.save()
                    form.save()
                    print('ew q : {}'.format(newq))

                    messages.success(request, 'Order Has Been Updated')
                    return redirect("orders:list_order")

                else:
                    new_order = get_order(order.order_id)

                    print("new quantity :{}".format(new_order.quantity))

                    newq = form.instance.quantity-old_order.quantity
                    item.stock_on_hand = item.stock_on_hand - newq
                    item.save()
                    form.save()

                    messages.success(request, "Order has Been Updated")

                    return redirect("orders:list_order")
                    # return redirect("orders:list_order")

    context = {
        'form': form,

    }

    return render(request, 'orders/order_update.html', context)


def stock():
    if itemstock-newquantity < 1:
        return True
    else:
        return False


def quantity(formquantity, quantity):
    if formquantity > quantity:
        return True
    else:
        return False


def get_order(order_id):
    try:
        qs = Order.objects.filter(order_id=order_id)
        return qs[0]

    except:
        return None


def delete_view(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == "POST":

        order.delete()
        messages.success(request, "Item Has Been Deleted")
        return redirect('orders:list_order')


def generate_invoice_id():
       
       inv_code = my_uuid = uuid.uuid4()
       return "INV-{}".format(inv_code)


def create_invoice(order,invoice_id):
    inv=Invoice.objects.create(order=order,invoice_id=invoice_id)

    return inv


