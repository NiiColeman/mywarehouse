from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    is_warehouse_manager = models.BooleanField('manager status', default=False)
    is_warehouse_staff = models.BooleanField(
        'warehouse staff status', default=False)
