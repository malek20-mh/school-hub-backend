from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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

class MarkAllAsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # تحديث كل إشعارات المستخدم غير المقروءة لتصبح مقروءة
        request.user.notifications.filter(is_read=False).update(is_read=True)
        return Response({"message": "All marked as read"}, status=status.HTTP_200_OK)