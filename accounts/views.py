from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login
from django.views.generic import CreateView, UpdateView
from .forms import ManagerSignupForm, StaffSignupForm
from items.models import User


class ManagerSignUpView(CreateView):
    model = User
    form_class = ManagerSignupForm
    template_name = 'accounts/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'manager'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


def user_list(request):
    user = User.objects.all()
    form = ManagerSignupForm()
    context = {
        'users': user,
        'form': form
    }

    return render(request, "accounts/user_list.html", context)


class UserCreateView(CreateView):
    model = User
    form_class = ManagerSignupForm
    template_name = 'accounts/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'manager'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()

        return redirect('users')


class UserUpdateView(UpdateView):
    model = User
    template_name = "accounts/update_form.html"
    form_class=ManagerSignupForm()

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'manager'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()

        return redirect('users')

    
def user_detail_view(request,pk):
    user=get_object_or_404(User,pk=pk)
    form=ManagerSignupForm(request.POST or None ,instance=user)

    context={
        'user':user,
        'form':form
    }
    
    return render(request,'accounts/user_detail.html',context)



# class UserDeleteView(DeleteView):
#     model = User
#     template_name = "accounts/user_list.html"
    
