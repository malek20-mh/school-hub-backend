from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import League
from notifications.models import Notification

User = get_user_model()

@receiver(post_save, sender=League)
def create_league_notification(sender, instance, created, **kwargs):
    if created:  # فقط عند إنشاء دوري جديد
        message = f"تم افتتاح دوري جديد: {instance.name}. سارع بالتسجيل!"
        
        # جلب جميع المستخدمين (أو مجموعة محددة)
        users = User.objects.all()
        
        # إنشاء إشعارات بالجملة (Bulk Create) لأداء أسرع
        notifications = [
            Notification(
                recipient=user,
                title="دوري جديد 🔥",
                message=message,
                notification_type='league_start'
            ) for user in users
        ]
        
        Notification.objects.bulk_create(notifications)