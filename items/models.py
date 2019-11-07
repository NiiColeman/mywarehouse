from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from departments.models import Department


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


class Item(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(
        Category, related_name='categories', on_delete=models.CASCADE)
    stock_on_hand = models.IntegerField(default=0)
    expiry_date = models.DateField(auto_now=False)
    shelf_number = models.CharField(max_length=50)
    description = models.CharField(max_length=450)
    perishable = models.BooleanField(default=False)

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
