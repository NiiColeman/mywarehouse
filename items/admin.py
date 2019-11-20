from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models import Category, Item, User, ItemSetting, StoreItem


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(ItemSetting)


@admin.register(StoreItem)
class StoreItemAdmin(ImportExportModelAdmin):
    pass
