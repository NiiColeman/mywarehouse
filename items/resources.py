from import_export import resources, fields
from .models import Category, Item, User
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget


class CategoryResource(resources.ModelResource):

    class Meta:
        Model = Category
        fields = ('name',)
