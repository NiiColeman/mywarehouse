from django.urls import path
from .views import department_list, DepartmentCreateView, DepartmentUpdateView, DepartmentDeleteView, DepartmentDetailView, department_detail_view


app_name = "departments"

urlpatterns = [
    path("department-list", department_list, name="department_list"),
    path("add-department", DepartmentCreateView.as_view(), name="add_department"),
    path("<int:pk>/update-department",
         DepartmentUpdateView.as_view(), name="update_department"),
    # path("<int:pk>/department-detail", DepartmentDetailView.as_view(), name="department_detail"),
    path("<int:pk>/department-detail",
         department_detail_view, name="department_detail"),


    path("<int:pk>/delete-department",
         DepartmentDeleteView.as_view(), name="delete_department"),

]
