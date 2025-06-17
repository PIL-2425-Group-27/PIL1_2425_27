from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Notification
from .serializers import NotificationSerializer, MarkNotificationReadSerializer
from django.utils import timezone

#  Liste paginée des notifications
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


#  Détail d’une seule notification
class NotificationDetailView(generics.RetrieveAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


# Marquer une notification comme lue
class MarkNotificationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = MarkNotificationReadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        notif_id = serializer.validated_data['notification_id']
        notification = get_object_or_404(Notification, id=notif_id, user=request.user)
        notification.is_read = True
        notification.read_at = notification.read_at or timezone.now()
        notification.save()
        return Response({"message": "Notification marquée comme lue."}, status=status.HTTP_200_OK)


# Marquer toutes les notifications comme lues
class MarkAllNotificationsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        updated = Notification.objects.filter(user=request.user, is_read=False).update(
            is_read=True, read_at=timezone.now()
        )
        return Response({"message": f"{updated} notifications marquées comme lues."}, status=status.HTTP_200_OK)
