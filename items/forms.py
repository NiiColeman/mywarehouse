from django import forms
from .models import Category,User,Item


class DateInput(forms.DateInput):
    input_type='date'

class ItemForm(forms.ModelForm):
    




   
 
    class Meta:
        widgets={'expiry_date':DateInput()}
        model = Item
        exclude = ('user','expired')
