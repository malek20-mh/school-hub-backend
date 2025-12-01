from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta, datetime
from psycopg2.extras import DateTimeTZRange

from .models import Stadium, Field, Booking, Maintenance
from .forms import FieldForm, MaintenanceForm, BookingForm


# 🏟️ قائمة الملاعب مع الفلترة
@login_required
def stadium_list(request):
    search_date = request.GET.get("search_date")
    search_time = request.GET.get("search_time")
    duration = int(request.GET.get("duration", 90))

    stadiums = Stadium.objects.all()
    available_fields = []

    if search_date and search_time:
        start_dt = datetime.strptime(f"{search_date} {search_time}", "%Y-%m-%d %H:%M")
        end_dt = start_dt + timedelta(minutes=duration)
        timeslot = DateTimeTZRange(start_dt, end_dt, "[)")

        for f in Field.objects.all():
            overlapping = Booking.objects.filter(
                field=f,
                timeslot__overlap=timeslot,
                status__in=["confirmed", "deposit_held"],
            ).exists()
            if not overlapping:
                available_fields.append(f)

    return render(request, "stadiums/stadium_list.html", {
        "stadiums": stadiums,
        "search_date": search_date,
        "search_time": search_time,
        "duration": duration,
        "available_fields": available_fields
    })


# 📋 تفاصيل الملعب (يوم واحد مع خيار عرض المتاح فقط)
@login_required
def stadium_detail(request, stadium_id):
    stadium = get_object_or_404(Stadium, id=stadium_id)
    day = request.GET.get("day")
    only_available = request.GET.get("only_available")

    if day:
        day = datetime.strptime(day, "%Y-%m-%d").date()
    else:
        day = timezone.now().date()

    all_fields = []
    for field in stadium.fields.all():
        slots = field.generate_daily_slots(day)

        # ربط بيانات الحجز
        for slot in slots:
            if slot["booking_id"]:
                slot["booking"] = Booking.objects.filter(id=slot["booking_id"]).first()
            else:
                slot["booking"] = None

        if only_available:
            slots = [s for s in slots if s["status"] == "available"]

        all_fields.append({"field": field, "slots": slots})

    return render(request, "stadiums/stadium_detail.html", {
        "stadium": stadium,
        "day": day,
        "only_available": only_available,
        "all_fields": all_fields
    })


# 📅 جدول أسبوعي للملعب
@login_required
def field_schedule(request, field_id):
    field = get_object_or_404(Field, id=field_id)
    start_day = timezone.now().date()
    days = [start_day + timedelta(days=i) for i in range(7)]

    week_slots = []
    for d in days:
        slots = field.generate_daily_slots(d)

        # ربط بيانات الحجز
        for slot in slots:
            if slot["booking_id"]:
                slot["booking"] = Booking.objects.filter(id=slot["booking_id"]).first()
            else:
                slot["booking"] = None

        week_slots.append({"day": d, "slots": slots})

    return render(request, "stadiums/field_schedule.html", {
        "field": field,
        "week_slots": week_slots
    })


# 📝 إنشاء حجز
@login_required
def create_booking(request, field_id):
    field = get_object_or_404(Field, id=field_id)

    if request.method == "POST":
        start = datetime.strptime(request.POST.get("start"), "%Y-%m-%d %H:%M")
        end = start + timedelta(minutes=90)
        timeslot = DateTimeTZRange(start, end, "[)")

        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.field = field
            booking.user = request.user
            booking.timeslot = timeslot
            booking.status = "pending"
            booking.save()
            messages.info(request, "✅ تم إرسال طلب الحجز مع بياناتك، بانتظار موافقة مدير الملعب.")
            return redirect("stadium_detail", stadium_id=field.stadium.id)
    else:
        form = BookingForm()

    return render(request, "stadiums/create_booking.html", {"form": form, "field": field})


# ✅ رفض/قبول الحجز
@login_required
def booking_action(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.user != booking.field.stadium.owner:
        return redirect("stadium_list")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "approve":
            booking.status = "confirmed"
            booking.save()
            messages.success(request, "✅ تم تأكيد الحجز.")

        elif action == "reject":
            booking.delete()  # الحذف = يرجع الوقت متاح
            messages.warning(request, "❌ تم رفض الحجز وإرجاع الفترة متاحة.")

    return redirect("stadium_detail", stadium_id=booking.field.stadium.id)


# ✏️ تعديل ملعب
@login_required
def edit_field(request, field_id):
    field = get_object_or_404(Field, id=field_id, stadium__owner=request.user)
    if request.method == "POST":
        form = FieldForm(request.POST, request.FILES, instance=field)  # ✅ دعم رفع الصور
        if form.is_valid():
            form.save()
            messages.success(request, "✅ تم تحديث بيانات الملعب.")
            return redirect("stadium_detail", stadium_id=field.stadium.id)
    else:
        form = FieldForm(instance=field)
    return render(request, "stadiums/edit_field.html", {"form": form, "field": field})


# 🛠️ إضافة صيانة
@login_required
def add_maintenance(request, field_id):
    field = get_object_or_404(Field, id=field_id)
    if request.user != field.stadium.owner:
        return redirect("stadium_list")

    if request.method == "POST":
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.field = field
            start, end = maintenance.timeslot.lower, maintenance.timeslot.upper
            maintenance.timeslot = DateTimeTZRange(start, end, "[)")
            maintenance.save()
            messages.success(request, "🛠️ تم إضافة فترة الصيانة.")
            return redirect("stadium_detail", stadium_id=field.stadium.id)
    else:
        form = MaintenanceForm()

    return render(request, "stadiums/add_maintenance.html", {"field": field, "form": form})


# 🛠️ تعديل صيانة
@login_required
def edit_maintenance(request, booking_id):
    maintenance = get_object_or_404(Maintenance, id=booking_id)
    if request.user != maintenance.field.stadium.owner:
        return redirect("stadium_list")

    if request.method == "POST":
        form = MaintenanceForm(request.POST, instance=maintenance)
        if form.is_valid():
            m = form.save(commit=False)
            start, end = m.timeslot.lower, m.timeslot.upper
            m.timeslot = DateTimeTZRange(start, end, "[)")
            m.save()
            messages.success(request, "🛠️ تم تعديل فترة الصيانة.")
            return redirect("stadium_detail", stadium_id=maintenance.field.stadium.id)
    else:
        form = MaintenanceForm(instance=maintenance)

    return render(request, "stadiums/edit_maintenance.html", {
        "form": form,
        "field": maintenance.field,
        "booking": maintenance
    })


# ❌ حذف صيانةس
@login_required
def delete_maintenance(request, booking_id):
    maintenance = get_object_or_404(Maintenance, id=booking_id)
    if request.user != maintenance.field.stadium.owner:
        return redirect("stadium_list")

    stadium_id = maintenance.field.stadium.id
    maintenance.delete()
    messages.warning(request, "🗑️ تم حذف فترة الصيانة.")
    return redirect("stadium_detail", stadium_id=stadium_id)