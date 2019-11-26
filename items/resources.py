from import_export import resources,fields
from .models import Category, Item, User, StoreItem
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget



class StoreItemResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'name'))

    class Meta:
        model = StoreItem
        fields = ('name', 'quantity', 'image', 'category', )


class CategoryResource(resources.ModelResource):

    class Meta:
        Model=Category
        fields=('name',)