from django.urls import path
from user.views import RegisterView,LoginView, manager_dashboard,employee_dashboard,LogoutView,profile,leave

urlpatterns = [
    path('',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('manager/dashboard/', manager_dashboard, name='manager_dashboard'),
    path('employee/dashboard/', employee_dashboard, name='employee_dashboard'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('profile/',profile,name='profile'),
    path('leave',leave,name='leave'),

]
