from django.urls import path
from .views import department_list


app_name = "departments"

urlpatterns = [
    path("department-list", department_list, name="department_list")
]
