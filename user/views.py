from django.views import View
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from .models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


class RegisterView(View):

    template_name = "user/register.html"
    form_class = RegisterForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        print(form)

        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect("login")
        messages.error(request, "Registration failed. Please check your details.")

        return render(request, self.template_name, {"form": form})

class LogoutView(View):
    def get(self,request):
        request.session.flush()
        messages.success(request, "Logout successfully.")
        return redirect('login')


class LoginView(View):

    template_name = "user/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        print(user)  # For debugging

        if user is not None:
            login(request, user)

            if user.role == User.Roles.MANAGER:
                messages.success(request, "Welcome Manager!")
                return redirect('manager_dashboard')
            else:
                messages.success(request, "Welcome Employee!")
                return redirect('employee_dashboard')

        else:
            messages.error(request, "Invalid email, password, or unverified account.")
            return render(request, self.template_name)


@login_required
def manager_dashboard(request):

    if request.user.role != User.Roles.MANAGER:
        return redirect("login")

    return render(request, "dashboard/dashboard.html")


@login_required
def employee_dashboard(request):

    if request.user.role != User.Roles.EMPLOYEE:
        return redirect("login")

    return render(request, "dashboard/dashboard.html")


def profile(request):
    return render(request, "user/profile.html")

def leave(request):
    return render(request, "user/leave.html")