from django.shortcuts import render
from items.models import Item, User, Category
from orders.models import Order
from departments.models import Department
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
import json
from datetime import datetime, timedelta


class ItemChart(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        date_me = datetime.now()+timedelta(60)
        expiring_product = Item.objects.filter(
            expiry_date__lte=date_me)
        expired = Item.objects.filter(expiry_date__lte=datetime.now())

        """
        Return a list of all users.
        """
        labels = ['Expiring Items', 'Expired Items', 'All Items']
        items = Item.objects.all()
        print(items.count())
        print(items)
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
            # print(l)
        print(label1)
        print(defaultData)
        # list_data_json = json.dumps(list(items.stock_on_hand))
        default = [expiring, expired, items]
        data = {
            'sales': 100,
            'customers': 10,
            'labels': labels,
            'default': default,
            'label1':label1,
            'data2':defaultData,


        }
        return Response(data)


def chartview(request):

    return render(request, 'chart.html')
