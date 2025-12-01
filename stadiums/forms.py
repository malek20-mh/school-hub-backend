from django import forms
from .models import Field, Maintenance, Booking, StadiumImage


# ✅ فورم تعديل بيانات الملعب الفرعي
class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ["name", "opening_time", "closing_time", "price_per_slot", "area"]
        widgets = {
            "opening_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "closing_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "price_per_slot": forms.NumberInput(attrs={"class": "form-control"}),
            "area": forms.NumberInput(attrs={"class": "form-control", "placeholder": "المساحة بالمتر المربع"}),
        }


# ✅ فورم إضافة / تعديل الصيانة
class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ["timeslot", "reason"]
        widgets = {
            "timeslot": forms.TextInput(
                attrs={"placeholder": "اكتب الفترة بصيغة: [YYYY-MM-DD HH:MM, YYYY-MM-DD HH:MM]", "class": "form-control"}
            ),
            "reason": forms.TextInput(attrs={"placeholder": "مثال: صيانة عشب، كهرباء...", "class": "form-control"})
        }


# ✅ فورم إنشاء الحجز (مع بيانات المستخدم)
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["full_name", "age", "address", "phone"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "الاسم الكامل"}),
            "age": forms.NumberInput(attrs={"class": "form-control", "placeholder": "العمر"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "الموقع"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "رقم الهاتف"}),
        }


# 🖼️ فورم رفع صورة جديدة للاستاد
class StadiumImageForm(forms.ModelForm):
    class Meta:
        model = StadiumImage
        fields = ["image", "caption"]
        widgets = {
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "caption": forms.TextInput(attrs={"class": "form-control", "placeholder": "وصف الصورة (اختياري)"}),
        }