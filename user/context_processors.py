
from django.utils import timezone
from .models import Notification

def notification_context(request):
    if request.user.is_authenticated:
        # All notifications (for dropdown)
        all_notifications = Notification.objects.filter(user=request.user)

        # Only unseen (for badge)
        unread_notifications = all_notifications.filter(seen=False)

        return {
            "notification_count": unread_notifications.count(),
            "recent_notifications": all_notifications
        }

    return {
        "notification_count": 0,
        "recent_notifications": []
    }