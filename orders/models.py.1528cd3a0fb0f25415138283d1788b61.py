from django.db import models
from items.models import Item, Category, User, ShelfItem
from django.shortcuts import reverse
from departments.models import Department
# Create your models here.
from django.shortcuts import reverse


class Order(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    shelf = models.ForeignKey(
        ShelfItem, on_delete=models.CASCADE)
    date_of_order = models.DateField(auto_now=False)
    order_id = models.CharField(unique=True, max_length=50)
    quantity = models.IntegerField(default=1)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    """Model definition for Order."""

    # TODO: Define fields here

    class Meta:

        """Meta definition for Order."""

        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        """Unicode representation of Order."""
        return self.shelf.item.name

    # def save(self):
    #     """Save method for Order."""
    #     pass
    # GET THE ORDER DETAIL URL
    def get_absolute_url(self):

        return reverse('orders:order_detail', kwargs={'pk': self.pk})

    # GET THE UPDATEBURL
    def get_update_url(self):

        return reverse('orders:order_update', kwargs={'pk': self.pk})

    # GET THE DELETE URL
    def get_delete_url(self):

        return reverse('orders:order_delete', kwargs={'pk': self.pk})

    # TODO: Define custom methods here
