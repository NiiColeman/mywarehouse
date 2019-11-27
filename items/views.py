from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from .forms import ItemForm,CategoryForm,MoveToFormShelf,ShelfItemForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView,CreateView
from .models import Item, User, Category,ItemSetting,ShelfItem
from datetime import datetime, timedelta
from django.http import JsonResponse
from .filters import ItemFilter
from orders.models import Order
from datetime import datetime
from django.db.models import Count
from django.db.models.functions import Trunc
from django.contrib.auth.decorators import user_passes_test
from tablib import Dataset
from .resources import CategoryResource


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
    today=datetime.now()

    expiring_product = Item.objects.filter(
        expiry_date__lte=date_me)
    expired = Item.objects.filter(expiry_date__lte=datetime.now())

    context = {
        'items': items,

        
        'expired': expired,
        'form':form,
        'today':today
        
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
    order_rel=item.order_set.all()
    print(" order _rel : {}".format(order_rel))


    context = {
        'item': item,
        'form': form
    }

    return render(request, 'items/item_detail.html', context)

@login_required
def expiring_list(request):
    sett = ItemSetting.objects.all()[0]
    # low_limit=sett.low_stock_limit
    exp_limit=sett.item_expiration_limit
    # print(exp_limit)
    # print(low_limit)
    items = Item.objects.all()
    date_me = datetime.now()+timedelta(exp_limit)
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
    sett = ItemSetting.objects.all()[0]
    low_limit=sett.low_stock_limit
    items=Item.objects.filter(stock_on_hand__lte=low_limit)


    return render(request,'items/low_stock.html',{'items':items})




class CategoryCreateView(CreateView):
    model = Category
    form_class=CategoryForm
    template_name = "category/category_form.html"

    def form_valid(self,form):


        form.save()
        messages.success(self.request,'Category has been added')
        return redirect('items:category_list')


class CategoryUpdateView(UpdateView):
    model = Category
    form_class=CategoryForm
    template_name = "category/category_update.html"

    def form_valid(self,form):
        form.save()
        messages.success(self.request,'Category has been updated')
        return redirect('items:update_category', pk=self.object.pk)

def delete_category(request,pk):
    cat=get_object_or_404(Category,pk=pk)

    if request.method=="POST":
        cat.delete()

        messages.success(request,'Category has been deleted')
        return reedirect('items:category_list')

        

def cat_list(request):
    cat=Category.objects.all()
    form=CategoryForm()

    context={
        'cats':cat,
        'form':form
    }

    return render(request,'category/category_list.html',context)




def category_detail(request,pk):
    cat=get_object_or_404(Category,pk=pk)
    form=CategoryForm()

    context={
        'cat':cat,
        'form':form

    }

    return render(request,'category/category_details.html',context)



# def simple_upload(request):
#     if request.method == 'POST':
#         storeitems_resource = StoreItemResource()
#         dataset = Dataset()
#         new_storeitems = request.FILES['myfile']

#         imported_data = dataset.load(new_storeitems.read())
#         result = storeitems_resource.import_data(dataset, dry_run=True)  # Test the data import

#         if not result.has_errors():
#             storeitems_resource.import_data(dataset, dry_run=False)  # Actually import now

#     return render(request, 'snippets/simple_upload.html')




def category_upload(request):
    if request.method == 'POST':
        category_resource = CategoryResource()
        dataset = Dataset()
        new_category = request.FILES['myfile']

        imported_data = dataset.load(new_category.read())
        result = category_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            category_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'snippets/simple_upload.html')







def item_page(request):
    form=ItemForm()

    context={
        'form':form

    }

    return render(request,'items/add_items.html',context)
    




def post_item(request):
    if request.method=="POST" and request.is_ajax():
        form=ItemForm(request.POST or None , request.FILES or None)
        user=request.user
        print(user)

        
      
        form.instance.user=user
        form.save()

        return JsonResponse({'success':True},status=200)

        
    
    return JsonResponse({'success':False},status=400)


def get_category(value):
    qs=Category.objects.filter(name=value)
    if qs:
        return qs[0]
    else:
        
        qs=Category.objects.create(name=value)
        return qs[0]
    


def shelf_list(request):
    shelfs=ShelfItem.objects.all()
    context={
        'shelfs':shelfs

    }

    return render(request,'shelf/shelfs.html',context)


def add_to_shelf(request):
    form=ShelfItemForm()

    if request.method=="POST":
        form=ShelfItemForm(request.POST or None)
        if form.is_valid():
            form.instance.user=request.user
            item=Item.objects.get(name=form.instance.item)

           
            
            if item.stock_on_hand < form.instance.quantity:
                
                messages.success(request,"Error! Maximum quantiy that can be moved to the shelf is {}".format(item.stock_on_hand))

                return redirect('/')
            elif item.stock_on_hand < 5:
                messages.success(request, 'Item is low on stock, only {} remaining'.format(item.stock_on_hand))
                return redirect('orders:list_order')
            else:
                print('good')
                shelf=shelf_items(form.instance.item)
                if shelf:
                    shelf.quantity=shelf.quantity + form.instance.quantity
                    shelf.shelf=form.instance.shelf
                    shelf.save()
                    item.stock_on_hand=item.stock_on_hand-form.instance.quantity
                    item.save()
                    messages.success(request,'I{} has been updated successfully'.format(form.instance.item))
                    return redirect('/')
                else:
                    item.stock_on_hand=item.stock_on_hand-form.instance.quantity
                    item.save()
                    form.save()
                    messages.success(request,'I{} has been added successfully'.format(form.instance.item))
                    return redirect('/')
                

                
        else:
            form=ShelfItemForm()

    
    context={
        'form':form
    }
    return render(request,'shelf/add_to_shelf.html',context)
        


        


        

def shelf_items(value):
    try:
        qs=ShelfItem.objects.filter(item=value)
        return qs[0]
    except:
        return None
        
    


            
        

     