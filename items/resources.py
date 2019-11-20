from import_export import resources
from .models import Category,Item,User,StoreItem




class StoreItemResource(resources.ModelResource):
    class Meta:
        model = StoreItem
        fileds=('name','quantity')
    



