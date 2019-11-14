from django import forms
from django.contrib.auth.forms import UserCreationForm
from items.models import User
from django.db import transaction


class ManagerSignupForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        # fields = ("username", "email", "first_name", "last_name")
        fields = ('__all__')

    @transaction.atomic
    def save(self):

        user = super().save(commit=False)
        user.is_warehouse_manager = True
        user.save()

        return user


class StaffSignupForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("__all__")

    @transaction.atomic
    def save(self):

        user = super().save(commit=False)
        user.is_warehouse_staff = True
        user.save()

        return user
