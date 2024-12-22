from django.urls import path
from .views import NotificationListView, MarkNotificationsAsReadView

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/mark-read/', MarkNotificationsAsReadView.as_view(), name='mark-notifications-read'),
]
