from django.db import models
from django.conf import settings

class Notification(models.Model):
    # أنواع الإشعارات (للتوسع مستقبلاً)
    NOTIFICATION_TYPES = (
        ('league_start', 'بداية دوري'),
        ('new_match', 'مباراة جديدة'),
        ('team_joined', 'فريق انضم'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='league_start')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # الأحدث أولاً

    def __str__(self):
        return f"{self.title} - {self.recipient}"