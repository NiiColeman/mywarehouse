from django import forms
from .models import Department


class DepartmentForm(forms.ModelForm):
    """Form definition for Department."""

    class Meta:
        """Meta definition for Departmentform."""

        model = Department
        fields = ('__all__')
