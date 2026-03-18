from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .manager import CustomUserManager
import datetime
from django.utils import timezone


class User(AbstractUser):
    class Roles(models.TextChoices):
        MANAGER = "MANAGER", "Manager"
        EMPLOYEE = "EMPLOYEE", "Employee"

    username = None
    email = models.EmailField(max_length=50,unique=True)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=Roles.choices)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} {self.get_role_display()}"


class UserProfile(models.Model):
    class Department(models.TextChoices):
        SALES = 'Sales', 'Sales'
        IT = 'IT', 'IT'
        HR = 'HR', 'HR'
        FINANCE = 'Finance', 'Finance'
        MARKETING = 'Marketing', 'Marketing'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.CharField(max_length=50, choices=Department.choices)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    join_date = models.DateField()
    last_notification_check = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.email} Profile"


class UserLeave(models.Model):
    class Status(models.TextChoices):
        PENDING = 'P', 'Pending'
        APPROVED = 'A', 'Approved'
        REJECTED = 'R', 'Rejected'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()

    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.email} - {self.get_status_display()}"


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    announce_date = models.DateField(default=datetime.date.today)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

class Notification(models.Model):
    class NotificationStatus(models.TextChoices):
        LEAVE = 'leave', 'Leave'
        ANNOUNCEMENT = 'announcement', 'Announcement'
        INFO = 'info', 'Info'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    seen = models.BooleanField(default=False)
    type = models.CharField(max_length=20, choices=NotificationStatus.choices,default=NotificationStatus.INFO)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message[:30]}"

