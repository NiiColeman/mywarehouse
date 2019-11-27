from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView,View
# Create your views here.
from .models import Order
from .forms import OrderForm
from items.models import Item,ShelfItem
from departments.models import Department
from django.contrib import messages
from invoices.models import Invoice
import uuid
from .filters import OrderFilter
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = "orders/new_order.html"

    def form_valid(self, form):

        shelf = ShelfItem.objects.get(item__name=form.instance.shelf)
        shelf.quantity = shelf.quantity-form.instance.quantity

        if shelf.quantity < form.instance.quantity:

            messages.success(
                    self.request, 'Order cannot be placed, requested items are more than the items in your inventory. Maximum quantity-{} that can be requested'.format(shelf.quantity))
            return redirect('orders:list_order')

        elif shelf.quantity < 1:
            messages.success(self.request, 'Item is low on stock')
            return redirect('orders:list_order')

        else:
            order_id = generate_random_string(shelf.item.name)
            form.instance.order_id = order_id
            shelf.save()
            form.instance.user=self.request.user
            form.save()
            order = get_order(order_id=order_id)
            invoice_id = invoice_id = generate_invoice_id()
            create_invoice(order, invoice_id)
            messages.success(
                self.request, 'Order Has Been Made')
            return redirect("orders:list_order")


class OrderListView(ListView):
    model = Order
    template_name = "orders/order_list.html"


def order_list_view(request):
    form = OrderForm()
    orders = Order.objects.all()
    items = Item.objects.all()
    departments = Department.objects.all()

    context = {
        'items': items,
        'departments': departments,
        'orders': orders,
        'form': form
    }

    return render(request, 'orders/order_list.html', context)


def generate_random_string(item):
    item_name = item.replace(' ', '-')
    rand_code = my_uuid = uuid.uuid4()
    return "{}-{}".format(item_name, rand_code)


# display the details of the order
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = OrderForm(request.POST or None, instance=order)

    context = {
        'order': order,
        'form': form
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
            shelf = ShelfItem.objects.get(item__name=form.instance.shelf)

            if shelf.quantity < form.instance.quantity:

                messages.success(
                    request, 'Order cannot be placed, requested items are more than the items in your inventory. Maximum quantity-{} that can be requested'.format(shelf.quantity))
                return redirect('orders:list_order')

            elif shelf.quantity < 1:
                messages.success(request, 'Item is low on stock')
                return redirect('orders:list_order')

            else:
                old_order = get_order(order.order_id)

                if form.instance.quantity < old_order.quantity:
                    newq = old_order.quantity-form.instance.quantity
                    print('item stock on hand : {}'.format(shelf.quantity))
                    shelf.quantity = shelf.quantity + newq
                    # print('item stock on hand : {}'.format(shelf.quantity))

                    shelf.save()
                    form.save()
                    # print('ew q : {}'.format(newq))

                    messages.success(request, 'Order Has Been Updated')
                    return redirect("orders:list_order")

                else:
                    new_order = get_order(order.order_id)

                    print("new quantity :{}".format(new_order.quantity))

                    newq = form.instance.quantity-old_order.quantity
                    shelf.quantity = shelf.quantity - newq
                    shelf.save()
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


def create_invoice(order, invoice_id):
    inv = Invoice.objects.create(order=order, invoice_id=invoice_id)

    return inv


def search(request):
    orders = Order.objects.all()
    order_filter = OrderFilter(request.GET, queryset=orders)

    context = {
        'filter': order_filter
    }

    return render(request, 'orders/search.html', context)




def create_order(request):
    data=dict()
    orders=Order.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            item = Item.objects.get(name=form.instance.item)
            order_id = generate_random_string(item.name)
            form.instance.order_id = order_id
            form.save()
            data['form_is_valid'] = True
            data['html_order_list'] = render_to_string('orders/mylist.html', {
                'orders': orders
            })
        else:
            data['form_is_valid'] = False
    else:
        form = OrderForm()
    
    context={
        'form':form,
        'orders':orders
    }
    data['html_form']=render_to_string('snippets/order_create.html',context,request=request)

    return JsonResponse(data)


#     form=OrderForm()





#     context={'form':form}
#     html_form=render_to_string('snippets/order_create.html',context,request=request)
#     return JsonResponse({'html_form':html_form})

def list_order(request):
    order=Order.objects.all()
    context={
        'orders':order
    }

    return render(request,'orders/list.html',context)



def save_order_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            orders = Order.objects.all()
            data['html_order_list'] = render_to_string('orders/mylist.html', {
                'orders': orders
            #     messages.success(request, "success")
            # return redirect('orders:list')
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)



def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
    else:
        form = OrderForm(instance=order)
    return save_order_form(request, form, 'snippets/myupdate.html')


def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    data = dict()
    if request.method == 'POST':
        order.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        orders = Order.objects.all()
        data['html_order_list'] = render_to_string('orders/mylist.html', {'orders': orders})
    else:
        context = {'order': order}
        data['html_form'] = render_to_string('snippets/delete_order.html',
            context,
            request=request,
        )
    return JsonResponse(data)