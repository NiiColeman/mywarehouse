from django.db import models
from orders.models import Order
# Create your models here.

class Invoice(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    date_added=models.DateTimeField(auto_now=True)
    invoice_id=models.CharField(max_length=250,unique=True,blank=True)
    """Model definition for Invoice."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for Invoice."""

        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'

    def __str__(self):
        """Unicode representation of Invoice."""
        return self.order.item.name

    

    # TODO: Define custom methods here
