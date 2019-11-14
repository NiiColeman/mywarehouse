from django import forms
from items.models import Item
from departments.models import Department


from .models import Order
choice=Department.objects.all()

class DateInput(forms.DateInput):
    input_type = 'date'


class OrderForm(forms.ModelForm):
    # department = forms.ModelChoiceField(widget=forms.Select(
    #    attrs={'class': 'js-states form-control', 'placeholder': 'Select Department','tabindex':-1,'display':"None",'width':"100%"}), required=True,queryset=choice)
    # item = forms.ChoiceField(widget=forms.Select(
    #    attrs={'class': 'js-states form-control', 'placeholder': 'Select Item'}), required=True)

    class Meta:
        model = Order
        widgets = {'date_of_order': DateInput()}
        fields = ("department", "item", "date_of_order", "quantity", "total")
