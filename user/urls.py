from django.urls import path
from user.views import (RegisterView,
                        LoginView,
                        DashboardView,
                        LogoutView,
                        LeaveView,
                        LeaveListView,
                        AnnouncementListView,
                        AnnounceView,
                        ProfileListView,
                        ProfileEditView, LeaveRequestListView,LeaveActionView,manager_dashboard,employee_dashboard,mark_notifications_seen)


urlpatterns = [
    # path('',DashboardView.as_view(), name='dashboard'),
    path('',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('manager/dashboard/', manager_dashboard, name='manager_dashboard'),
    path('employee/dashboard/', employee_dashboard, name='employee_dashboard'),
    path('logout/',LogoutView.as_view(),name='logout'),

    path('leave',LeaveListView.as_view(),name='leave'),
    path('apply_leave',LeaveView.as_view(),name='apply_leave'),
    path('announce/',AnnouncementListView.as_view(),name='announce'),
    path('create_announcement/',AnnounceView.as_view(),name='create_announcement'),
    path('profile',ProfileListView.as_view(),name='profile'),
    path("edit_profile/",ProfileEditView.as_view(),name="edit_profile"),
    path('leave-requests/', LeaveRequestListView.as_view(), name='leave_requests'),
    path('leave-action/<int:pk>/', LeaveActionView.as_view(), name='leave_action'),
    path('notifications/mark_seen/', mark_notifications_seen, name='mark_notifications_seen'),

]
