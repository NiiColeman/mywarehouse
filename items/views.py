from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import wmanager_required, wstaff_required
from .forms import ItemForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
# Create your views here.
from django.views.generic import UpdateView, DeleteView
from .models import Item, User, Category
from datetime import datetime, timedelta
from django.http import JsonResponse
from .filters import ItemFilter
from orders.models import Order
from datetime import datetime
from django.db.models import Count
from django.db.models.functions import Trunc
from django.contrib.auth.decorators import user_passes_test

@login_required
def index(request):
    current_month = datetime.now().month
    monthly_orders = Order.objects.filter(date_of_order__month=current_month)
    print(monthly_orders)

    month_order = Order.objects.annotate(order_month=Trunc(
        'date_of_order', 'month')).values('order_month').annotate(orders=Count('id'))
    for orders in month_order:
        print("whats {}".format(orders['orders']))
    items=Item.objects.all()
    date_me = datetime.now()+timedelta(60)
    expiring_product = Item.objects.filter(
        expiry_date__lte=date_me)
    expired = Item.objects.filter(expiry_date__lte=datetime.now())

    return render(request, "items/index.html", {'monthly_orders':monthly_orders,'expiring_product':expiring_product,'expired':expired,'items':items})


@login_required
# @wmanager_required
@user_passes_test(lambda u: u.is_superuser)

def test_perm(request):
    form = ItemForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, 'item has been added')

            return redirect('items:item_list')

    context = {
        'form': form
    }

    return render(request, 'items/add_items.html', context)


class ItemUpdateView(UpdateView,LoginRequiredMixin):
    model = Item
    form_class = ItemForm
    template_name = "items/update.html"
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()

        messages.success(self.request, "Item has been updated")
        return redirect('items:item_list')

@login_required
def item_list(request):
    form=ItemForm()
    items = Item.objects.all()
    date_me = datetime.now()+timedelta(60)
    expiring_product = Item.objects.filter(
        expiry_date__lte=date_me)
    expired = Item.objects.filter(expiry_date__lte=datetime.now())

    context = {
        'items': items,
        # 'expring_products': expiring_product,
        'expired': expired,
        'form':form
    }
    print(date_me)
    print(expiring_product)
    print(datetime.now())

    return render(request, "items/item_list.html", context)

@login_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        item.delete()

        messages.success(request, 'Item has been deleted')
        return redirect('items:item_list')

    return redirect(request, 'snippets/delete_form.html')

@login_required
def item_detail_view(request, pk):

    item = get_object_or_404(Item, pk=pk)
    form = ItemForm(request.POST or None, request.FILES or None, instance=item)
    context = {
        'item': item,
        'form': form
    }

    return render(request, 'items/item_detail.html', context)

@login_required
def expiring_list(request):
    items = Item.objects.all()
    date_me = datetime.now()+timedelta(60)
    expiring_product = Item.objects.filter(
        expiry_date__lte=date_me)
    expired = Item.objects.filter(expiry_date__lte=datetime.now())

    context = {
        'items': items,
        'expiring_products': expiring_product,
        'expired': expired
    }
    print(date_me)
    print(expiring_product)
    print(datetime.now())

    return render(request, "items/expiring_items.html", context)


def get_items(request, *args, **kwargs):
    data = {
        "sales": 50,
        "report": 70
    }

    return JsonResponse(data)

@login_required
def search(request):
    items = Item.objects.all()
    item_filter = ItemFilter(request.GET, queryset=items)

    context = {
        'filter': item_filter
    }

    return render(request, 'items/search.html', context)




def low_stock(request):
    items=Item.objects.filter(stock_on_hand__lte=10)


    return render(request,'items/low_stock.html',{'items':items})