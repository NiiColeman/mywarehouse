from django import forms
from .models import Category, User, Item, ItemSetting, ShelfItem


class DateInput(forms.DateInput):
    input_type = 'date'


class ItemForm(forms.ModelForm):

    class Meta:
        widgets = {'expiry_date': DateInput()}

        model = Item
        exclude = ('user', 'expired')


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ("name",)


class ItemSettingForm(forms.ModelForm):
    """ItemSttingForm definition."""

    # TODO: Define form fields here
    class Meta:
        model = ItemSetting
        fields = ("low_stock_limit", "item_expiration_limit")


class ShelfItemForm(forms.ModelForm):

    class Meta:
        model = ShelfItem
        fields = ("item", "quantity", "shelf")


class MoveToFormShelf(forms.ModelForm):

    class Meta:
        model = ShelfItem
        fields = ("quantity", "shelf")
