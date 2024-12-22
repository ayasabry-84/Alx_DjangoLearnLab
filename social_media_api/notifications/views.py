from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user, read=False)
        data = [
            {
                "actor": notification.actor.username,
                "verb": notification.verb,
                "target": str(notification.target),
                "timestamp": notification.timestamp,
            }
            for notification in notifications
        ]
        return Response(data)

class MarkNotificationsAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Notification.objects.filter(recipient=request.user, read=False).update(read=True)
        return Response({"message": "All notifications marked as read."})
