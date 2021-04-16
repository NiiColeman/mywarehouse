from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView, UpdateView
from .forms import ManagerSignupForm, UpdateUserForm
from items.models import User
from django.contrib import messages


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

        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(self.request, "User has been successfully creatted")

        return redirect('users')


class UserUpdateView(UpdateView):
    model = User
    template_name = "accounts/update_form.html"
    form_class = ManagerSignupForm()

    def form_valid(self, form):
        form.save()

        return redirect('users')


def user_detail_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = UpdateUserForm(request.POST or None, instance=user)

    context = {
        'user': user,
        'form': form
    }

    return render(request, 'accounts/user_detail.html', context)


# class UserDeleteView(DeleteView):
#     model = User
#     template_name = "accounts/user_list.html"


def user_update_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = UpdateUserForm()

    if request.method == "POST":
        form = UpdateUserForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User has been successfully updated")

            return redirect('users')
        else:
            messages.success(request, "failed to update user")

            return redirect('users')

    else:
        form = ManagerSignupForm()
    context = {'form': form
               }
    return render(request, "accounts/update_user.html", context)
