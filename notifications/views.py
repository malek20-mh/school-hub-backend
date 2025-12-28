from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # المستخدم يرى فقط إشعاراته
        return Notification.objects.filter(recipient=self.request.user)

# فيو إضافي لتحديث الإشعار بأنه "تمت قراءته"
class MarkNotificationReadView(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_update(self, serializer):
        serializer.save(is_read=True)