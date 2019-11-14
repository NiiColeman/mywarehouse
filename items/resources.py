from import_export import resources
from .models import Category,Item,User





class ItemResource(resources.ModelResource):
    class Meta:
        model = Item
        fields=('user__username')