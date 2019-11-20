from django.shortcuts import render,get_object_or_404,redirect
from items.models import Item, User, Category
from orders.models import Order
from departments.models import Department
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
import json
from datetime import datetime, timedelta
from items.models import ItemSetting
from items.forms import ItemSettingForm
from django.contrib import messages

class ItemChart(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        date_me = datetime.now()+timedelta(60)
        expiring_product = Item.objects.filter(
            expiry_date__lte=date_me)
        expired = Item.objects.filter(expiry_date__lte=datetime.now())
        sett = ItemSetting.objects.all()[0]
        print(sett.low_stock_limit)
        print(sett.item_expiration_limit)

        """
        Return a list of all users.
        """
        labels = ['Expiring Items', 'Expired Items', 'All Items']
        items = Item.objects.all()

        items = items.count()
        expiring = expiring_product.count()
        expired = expired.count()

        departments = Department.objects.all()

        orders = Order.objects.all

        label1 = []
        defaultData = []
        for dept in departments:
            l = dept.department_name

            d = dept.order_set.all()
            defaultData.append(d.count())
            label1.append(l)
            print(d.count())

        default = [expiring, expired, items]
        data = {
            'sales': 100,
            'customers': 10,
            'labels': labels,
            'default': default,
            'label1': label1,
            'data2': defaultData,


        }
        return Response(data)


def chartview(request):

    return render(request, 'chart.html')





def settings_view(request):
    sett= ItemSetting.objects.all()[0]
    form=ItemSettingForm()
    context={
        'sett':sett,
        'form':form
    }

    return render(request, "items/settings.html",context)


def settings_update_view(request,pk):
    sett=get_object_or_404(ItemSetting,pk=pk)
    form=ItemSettingForm(request.POST or None)


    if request.method=="POST":
        form=ItemSettingForm(request.POST or None ,instance=sett)

        if form.is_valid():
            form.save()
            messages.success=(request,"settings have been updated")
            return redirect("item_settings")
        else:
            messages.success=(request,"failed to update settings")
            return redirect("item_settings")

        
    context={
        'form':form,
        'sett':sett
    }


    return render(request,"snippets/settings_form.html",context)
        