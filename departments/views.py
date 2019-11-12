from django.shortcuts import render
from django.views.generic import ListView,CreateView,UpdateView
from .models import Department
# Create your views here.



class DepartmentListView(ListView):
    model = Department
    template_name = "departments/department_list.html"



def department_list(request):
    department=Department.objects.all()
    context={
        'departments':department
    }

    return render(request,'departments/department_list.html',context)

    