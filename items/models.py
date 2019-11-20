from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from departments.models import Department
from django.shortcuts import reverse


class User(AbstractUser):
    is_warehouse_manager = models.BooleanField('manager status', default=False)
    is_warehouse_staff = models.BooleanField(
        'warehouse staff status', default=False)


class Category(models.Model):
    name = models.CharField(max_length=250)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """Unicode representation of Category."""
        return self.name

    def get_absolute_url(self):
        return reverse("items:category_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("items:update_category", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("items:category_delete", kwargs={"pk": self.pk})


class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(
        Category, related_name='categories', on_delete=models.CASCADE)
    stock_on_hand = models.IntegerField(default=0)
    expiry_date = models.DateField(auto_now=False)
    shelf_number = models.CharField(max_length=50)
    description = models.CharField(max_length=450)
    perishable = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Item."""

        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        """Unicode representation of Item."""
        return self.name

    def get_absolute_url(self):
        return reverse("items:item_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("items:item_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("items:item_delete", kwargs={"pk": self.pk})


class ItemSetting(models.Model):
    CHOICES = (
        (30, ("1 Months")),
        (60, ("2 Months")),
        (90, ("3 Months")),
        (120, ("4 Months"))

    )
    name = models.CharField(default="Item Settings", max_length=50)
    low_stock_limit = models.IntegerField(default=10)
    item_expiration_limit = models.IntegerField(choices=CHOICES, default=30)

    class Meta:
        verbose_name = ("Item Setting")
        verbose_name_plural = ("Item Settings")

    def __str__(self):
        return self.name


class StoreItem(models.Model):
    name = models.CharField(max_length=250)
    quantity = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now=True)

    """Model definition for StoreItem."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for StoreItem."""

        verbose_name = 'StoreItem'
        verbose_name_plural = 'StoreItems'

    def __str__(self):

        return self.name
