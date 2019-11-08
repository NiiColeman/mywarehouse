from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import wmanager_required, wstaff_required
from .forms import ItemForm
from django.contrib import messages
# Create your views here.
from django.views.generic import UpdateView, DeleteView
from .models import Item, User, Category
from datetime import datetime, timedelta


@login_required
def index(request):

    return render(request, "items/index.html", {})


@login_required
# @wmanager_required
def test_perm(request):
    form = ItemForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, 'item has been added')

            return redirect('items:add')

    context = {
        'form': form
    }

    return render(request, 'items/add_items.html', context)


class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm
    template_name = "items/update.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()

        messages.success(self.request, "Item has been updated")
        return redirect('items:item_list')


def item_list(request):
    items = Item.objects.all()
    date_me = datetime.now()+timedelta(60)
    expiring_product = Item.objects.filter(
        expiry_date__lte=date_me)
    expired = Item.objects.filter(expiry_date__lte=datetime.now())

    context = {
        'items': items,
        # 'expring_products': expiring_product,
        'expired': expired
    }
    print(date_me)
    print(expiring_product)
    print(datetime.now())

    return render(request, "items/item_list.html", context)


def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        item.delete()

        messages.success(request, 'Item has been deleted')
        return redirect('items:item_list')

    return redirect(request, 'snippets/delete_form.html')


def item_detail_view(request, pk):

    item = get_object_or_404(Item, pk=pk)
    form = ItemForm(request.POST or None, request.FILES or None, instance=item)
    context = {
        'item': item,
        'form': form
    }

    return render(request, 'items/item_detail.html', context)


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
