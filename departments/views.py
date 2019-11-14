from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Department
# Create your views here.
from .forms import DepartmentForm
from django.contrib import messages
from django.urls import reverse_lazy


class DepartmentListView(ListView):
    model = Department
    template_name = "departments/department_list.html"


def department_list(request):
    department = Department.objects.all()
    form = DepartmentForm()
    context = {
        'departments': department,
        'form': form
    }

    return render(request, 'departments/department_list.html', context)


class DepartmentCreateView(CreateView):
    model = Department
    template_name = "departments/department_form.html"
    form_class = DepartmentForm

    def form_valid(self, form):
        if check_departments(form.instance.department_name):
            messages.success(
                self.request, "This department name already exists")
            return redirect('departments:department_list')
        else:
            form.save()
            messages.success(self.request, "Department Has Been Added")
            return redirect('departments:department_list')


class DepartmentUpdateView(UpdateView):

    model = Department
    template_name = "departments/update_department.html"
    form_class = DepartmentForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Department Has Been Updated")

        return redirect("departments:department_detail", pk=self.object.pk)


class DepartmentDeleteView(DeleteView):
    model = Department
    template_name = "departments/delete_departments.html"


class DepartmentDetailView(DetailView):
    model = Department
    template_name = "departments/department_detail.html"


def department_detail_view(request, pk):

    dept = get_object_or_404(Department, pk=pk)
    form = DepartmentForm(request.POST or None, instance=dept)

    context = {
        'dept': dept,
        'form': form
    }

    return render(request, 'departments/department_detail.html', context)


def check_departments(department_name):

    try:
        qs = Department.objects.filter(department_name=department_name)

        return qs[0]

    except:
        return None
