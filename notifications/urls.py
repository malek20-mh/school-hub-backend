from django.urls import path
from .views import NotificationListView, MarkNotificationReadView, MarkAllAsReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='my-notifications'),
    path('<int:pk>/read/', MarkNotificationReadView.as_view(), name='mark-read'),
    path('mark-all-read/', MarkAllAsReadView.as_view(), name='mark-all-read'),
]