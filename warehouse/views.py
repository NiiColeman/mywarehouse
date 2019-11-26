from django.shortcuts import render, get_object_or_404, redirect
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
from items.forms import ItemForm
from django.http import JsonResponse
import openpyxl


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
    sett = ItemSetting.objects.all()[0]
    form = ItemSettingForm()
    context = {
        'sett': sett,
        'form': form,

    }
    return render(request, "items/settings.html", context)


def settings_update_view(request, pk):
    sett = get_object_or_404(ItemSetting, pk=pk)
    form = ItemSettingForm()

    if request.method == "POST":
        form = ItemSettingForm(request.POST or None, instance=sett)
        if form.is_valid():
            form.save()

            messages.success(request, "settings have been updated")
            return redirect('settings')

    context = {
        'form': form,
        'sett': sett
    }

    return render(request, "snippets/settings_form.html", context)


def upload_items(request):

    if request.method == "POST":
        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["Sheet1"]
        print(worksheet)

        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
                # print(row_data)
            excel_data.append(row_data)

        for i in excel_data:
            if i[1] == "category" or i[1] == "None":
                print('skip')
            elif not get_item(i[0]):
                print("skipping {}".format(i[0]))
                cat=get_category(i[1])
                item=Item.objects.create(user=request.user, name=i[0], category=cat, expiry_date=i[2], stock_on_hand=i[3])
                
                print(i)

        return render(request, 'upload_excel.html', {"excel_data": excel_data})
    else:
        return render(request, 'upload_excel.html')


def get_category(value):
    qs = Category.objects.filter(name=value)

    if qs:
        return qs[0]
    else:

        qs = Category.objects.create(name=value)
        return qs[0]


def get_item(value):
    try:
        qs = Item.objects.filter(name=value)
        return qs
    except:
        return None
