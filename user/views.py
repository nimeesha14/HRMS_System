from urllib import request
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, UserLeaveForm, AnnounceForm, ProfileForm
from django.contrib.auth import authenticate, login
from .models import User, UserLeave, Announcement, UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Notification


class RegisterView(View):
    """Handle user registration."""

    template_name = "user/register.html"
    form_class = RegisterForm

    def get(self, request: HttpRequest) -> HttpResponse:
        """Render registration form."""
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Process registration form submission."""
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect("login")

        messages.error(request, "Registration failed. Please check your details.")
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    """Handle user logout by clearing session."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Log out the user and redirect to login page."""
        request.session.flush()
        messages.success(request, "Logout successfully.")
        return redirect('login')


class LoginView(View):
    """Handle user authentication and role-based redirection."""

    template_name = "user/login.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """Render login page."""
        return render(request, self.template_name)

    def post(self, request: HttpRequest) -> HttpResponse:
        """Authenticate user and redirect based on role."""
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            if user.role == User.Roles.MANAGER:
                messages.success(request, "Welcome Manager!")
                return redirect('manager_dashboard')
            else:
                messages.success(request, "Welcome Employee!")
                return redirect('employee_dashboard')

        messages.error(request, "Invalid email, password, or unverified account.")
        return render(request, self.template_name)


@login_required
def manager_dashboard(request: HttpRequest) -> HttpResponse:
    """Render manager dashboard if user has manager role."""
    if request.user.role != User.Roles.MANAGER:
        return redirect("login")
    return render(request, "dashboard/dashboard.html")


@login_required
def employee_dashboard(request: HttpRequest) -> HttpResponse:
    """Render employee dashboard if user has employee role."""
    if request.user.role != User.Roles.EMPLOYEE:
        return redirect("login")
    return render(request, "dashboard/dashboard.html")


class DashboardView(View):
    """Render generic dashboard page."""

    template_name = "dashboard/dashboard.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """Display dashboard."""
        return render(request, self.template_name)


class LeaveView(View):
    """Handle leave application submission."""

    template_name = "user/apply_leave.html"
    form_class = UserLeaveForm

    def get(self, request: HttpRequest) -> HttpResponse:
        """Render leave application form."""
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class(request.POST)

        if form.is_valid():
            leave = form.save(commit=False)
        leave.user = request.user
        leave.save()

        managers = User.objects.filter(role=User.Roles.MANAGER)
        notifications = [
            Notification(
                user=manager,
                message=f"New leave request from {request.user.first_name} {request.user.last_name}",
                type=Notification.NotificationStatus.LEAVE
            )
            for manager in managers
        ]
        Notification.objects.bulk_create(notifications)

        messages.success(request, "User Leave Successfully!")
        return redirect("leave")

        messages.error(request, "User Leave Failed!")
        return render(request, self.template_name, {"form": form})


class LeaveListView(View):
    """Display list of leaves for logged-in user."""

    template_name = "user/leave.html"
    form_class = UserLeaveForm

    def get(self, request: HttpRequest) -> HttpResponse:
        """Fetch and display user leave records."""
        form = self.form_class()
        leaves = UserLeave.objects.filter(user=request.user).order_by("-created_at")
        return render(request, self.template_name, {"form": form, "leaves": leaves})


class AnnouncementView(View):
    """Render announcement page."""

    template_name = "user/announcement.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """Display announcement page."""
        return render(request, self.template_name)


class AnnounceView(View):
    """Handle creation of announcements and notify users."""

    template_name = "user/create_announcement.html"
    form_class = AnnounceForm

    def get(self, request: HttpRequest) -> HttpResponse:
        """Render announcement creation form."""
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Process announcement form submission and create notifications."""
        form = self.form_class(request.POST)

        if form.is_valid():
            announcement = form.save()  # Save the announcement


            employees = User.objects.filter(role=User.Roles.EMPLOYEE)
            notifications = [
                Notification(
                    user=employee,
                    message=f"New announcement: {announcement.title}",
                    type=Notification.NotificationStatus.ANNOUNCEMENT
                )
                for employee in employees
            ]
            Notification.objects.bulk_create(notifications)


            messages.success(request, "Announcement created and notifications sent!")
            return redirect("profile")

        messages.error(request, "Announcement Failed!")
        return render(request, self.template_name, {"form": form})


class AnnouncementListView(View):
    """Display list of all announcements."""

    template_name = "user/announcement.html"
    form_class = AnnounceForm

    def get(self, request: HttpRequest) -> HttpResponse:
        """Fetch and display announcements."""
        form = self.form_class()
        announcement = Announcement.objects.all()
        return render(request, self.template_name, {"form": form, "announcement": announcement})


class ProfileEditView(View):
    """Handle user profile creation and update."""

    template_name = "user/edit_profile.html"
    form_class = ProfileForm

    def get(self, request: HttpRequest) -> HttpResponse:
        """Render profile edit form with existing data."""
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        form = self.form_class(instance=profile)
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Update or create user profile."""
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        form = self.form_class(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile Successfully!")
            return redirect("profile")

        messages.error(request, "Profile Failed!")
        return render(request, self.template_name, {"form": form})


class ProfileListView(View):
    """Display logged-in user's profile."""

    template_name = "user/profile.html"
    form_class = ProfileForm

    def get(self, request: HttpRequest) -> HttpResponse:
        """Fetch and display profile details."""
        form = self.form_class()
        profile = UserProfile.objects.filter(user=request.user).first()
        return render(request, self.template_name, {"form": form, "profile": profile})


class LeaveRequestListView(View):
    """Allow manager to view all leave requests."""

    template_name = "user/leavelist_manager.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """Display all leave requests for manager."""
        if request.user.role != "MANAGER":
            return redirect("leave")

        leaves = UserLeave.objects.select_related('user', 'user__userprofile').all().order_by('-created_at')
        return render(request, self.template_name, {"leaves": leaves})


class LeaveActionView(View):
    """Handle leave approval or rejection by manager."""

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Approve or reject leave request and notify employee."""
        leave = get_object_or_404(UserLeave, id=pk)
        action = request.POST.get("action")

        if action == "approve":
            leave.status = UserLeave.Status.APPROVED
        elif action == "reject":
            leave.status = UserLeave.Status.REJECTED

        leave.save()


        Notification.objects.create(
            user=leave.user,
            message=f"Your leave from {leave.start_date} to {leave.end_date} was {leave.get_status_display().lower()}",
            type=Notification.NotificationStatus.LEAVE
        )

        return redirect("leave_requests")

#
# @login_required
# def mark_notifications_seen(request):
#     """Mark all notifications as seen by updating last_notification_check."""
#     profile, _ = UserProfile.objects.get_or_create(user=request.user)
#     Notification.objects.filter(user=request.user, seen=False).update(seen=True)
#     profile.save()
#     return redirect(request.META.get('HTTP_REFERER', '/'))

def mark_notifications_seen(request):
    if request.user.is_authenticated:
        Notification.objects.filter(user=request.user, seen=False).update(seen=True)

    return redirect(request.META.get('HTTP_REFERER', '/'))