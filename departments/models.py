from django.db import models
from django.shortcuts import reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
# Create your models here..


class Department(models.Model):
    """Model definition for Department."""
    department_name = models.CharField(max_length=250)
    department_head = models.CharField(max_length=250)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Department."""

        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        """Unicode representation of Department."""
        return self.department_name

    def get_absolute_url(self):
        return reverse("departments:department_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("departments:update_department", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("departments:delete_department", kwargs={"pk": self.pk})

    # TODO: Define custom methods here
