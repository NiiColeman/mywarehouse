from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models import Category, Item, User, ItemSetting, ShelfItem


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    pass


@admin.register(ShelfItem)
class ShelfItemAdmin(admin.ModelAdmin):
    '''Admin View for ShelfItem'''

    # list_display = ('',)
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)
    pass
