from datetime import datetime, timedelta, time

from django.db import models
from django.contrib.postgres.fields import DateTimeRangeField
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.indexes import GistIndex
from django.db.models import Q, F
from psycopg2.extras import DateTimeTZRange


# 🏟️ ملعب
class Stadium(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True, null=True)
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# ⚽ ملعب فرعي
class Field(models.Model):
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE, related_name="fields")
    name = models.CharField(max_length=100)

    # 🕒 أوقات العمل
    opening_time = models.TimeField(default=time(5, 30))
    closing_time = models.TimeField(default=time(23, 59))

    # 💰 السعر لكل فترة
    price_per_slot = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # 📐 مساحة الملعب (اختياري)
    area = models.PositiveIntegerField(blank=True, null=True, help_text="المساحة بالمتر المربع")

    def __str__(self):
        return f"{self.stadium.name} - {self.name}"

    # 🟢 توليد فترات اليوم (افتراضياً 90 دقيقة) مع حالة كل فترة
    def generate_daily_slots(self, day, slot_minutes=90):
        """
        يُولّد فترات اليوم بين opening_time و closing_time بحالة:
        available / pending / confirmed / canceled / expired
        """
        slots = []

        day_start = datetime.combine(day, self.opening_time)
        day_end = datetime.combine(day, self.closing_time)
        day_range = DateTimeTZRange(day_start, day_end, "[)")

        # ملاحظة مهمة: استخدم lookups الصحيحة: timeslotoverlap و statusin
        bookings = self.bookings.filter(timeslot__overlap=day_range)
        maints = self.maintenances.filter(timeslot__overlap=day_range)

        cursor = day_start
        step = timedelta(minutes=slot_minutes)

        while cursor + step <= day_end:
            slot_start = cursor
            slot_end = cursor + step
            slot_range = DateTimeTZRange(slot_start, slot_end, "[)")

            booking = bookings.filter(timeslot__overlap=slot_range).first()
            maintenance = maints.filter(timeslot__overlap=slot_range).first()

            if maintenance:
                status = "canceled"   # فترة تحت الصيانة = غير متاحة
                booking_id = None
            elif booking:
                status = booking.status  # pending / confirmed / canceled / expired / deposit_held
                booking_id = booking.id
            else:
                status = "available"
                booking_id = None

            slots.append({
                "start": slot_start,
                "end": slot_end,
                "status": status,
                "booking_id": booking_id,
                "price": self.price_per_slot,
            })

            cursor = slot_end

        return slots


# 📑 حجز
class Booking(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name="bookings")
    timeslot = DateTimeRangeField()  # (start, end) بصيغة [)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    # ✅ بيانات إضافية للمستخدم (اجعلها قابلة للإفراغ لتفادي مشاكل الميغريشن)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("deposit_held", "Deposit Held"),
            ("confirmed", "Confirmed"),
            ("canceled", "Canceled"),
            ("expired", "Expired"),
        ],
        default="pending",
    )
    class Meta:
        indexes = [GistIndex(fields=["timeslot"])]
        constraints = [
            ExclusionConstraint(
                name="exclude_overlapping_confirmed_bookings",
                expressions=[
                    (F("field"), "="),
                    (F("timeslot"), "&&"),
                ],
                # انتبه: lookup الصحيح هو status__in
                condition=Q(status__in=["confirmed", "deposit_held"]),
            )
        ]

    def __str__(self):
        return f"Booking for {self.field} by {self.user}"


# 🛠️ صيانة (وقت محجوب)
class Maintenance(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name="maintenances")
    timeslot = DateTimeRangeField()  # يُفضَّل استخدام [) عند الإنشاء
    reason = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Maintenance for {self.field} ({self.reason})"


# 🖼️ صور الملاعب
class StadiumImage(models.Model):
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="stadiums/")  # يتطلب Pillow
    caption = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.stadium.name}"