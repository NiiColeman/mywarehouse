from ajax_select import register, LookupChannel
from items.models import Item
from departments.models import Department


# @register('items')
# class ItemLookup(LookupChannel):

#     model = Item

#     def get_query(self, q, request):
#         return self.model.objects.filter(name__icontains=q).order_by('name')[:50]

#     def format_item_display(self, item):
#         return u"<span class='item'>%s</span>" % item.name


@register('departments')
class DepartmentLookup(LookupChannel):

    model = Department

    def get_query(self, q, request):
        return self.model.objects.filter(department_name__icontains=q).order_by('department_name')[:50]

    def format_item_display(self, item):
        return u"<span class='item'>%s</span>" % item.name
