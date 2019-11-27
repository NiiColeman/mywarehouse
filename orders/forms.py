from django import forms
from items.models import Item
from departments.models import Department
from ajax_select.fields import AutoCompleteSelectMultipleField
from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField


from .models import Order
choice = Department.objects.all()


class DateInput(forms.DateInput):
    input_type = 'date'


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        widgets = {'date_of_order': DateInput()}
        fields = ("department", "shelf", "date_of_order", "quantity")
