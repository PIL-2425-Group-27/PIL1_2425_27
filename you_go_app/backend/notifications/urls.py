from django.urls import path
from .views import (
    NotificationListView,
    NotificationDetailView,
    MarkNotificationReadView,
    MarkAllNotificationsReadView,
)

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('detail/', NotificationDetailView.as_view(), name='notification-detail'),
    path('read/', MarkNotificationReadView.as_view(), name='notification-mark-read'),
    path('allread/', MarkAllNotificationsReadView.as_view(), name='notification-mark-all-read'),
]
