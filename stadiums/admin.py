from django.contrib import admin
from .models import Stadium, Field, Booking, Maintenance, StadiumImage


class StadiumImageInline(admin.TabularInline):
    model = StadiumImage
    extra = 1


@admin.register(Stadium)
class StadiumAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'owner')
    search_fields = ('name', 'location', 'owner__username')
    inlines = [StadiumImageInline]


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'stadium', 'opening_time', 'closing_time', 'price_per_slot')
    list_filter = ('stadium',)
    search_fields = ('name', 'stadium__name')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('field', 'user', 'status')
    list_filter = ('status', 'field__stadium')
    search_fields = ('userusername', 'fieldname', 'fieldstadiumname')


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('field', 'timeslot', 'reason')
    list_filter = ('field__stadium',)
    search_fields = ('reason', 'fieldname', 'fieldstadium__name')


@admin.register(StadiumImage)
class StadiumImageAdmin(admin.ModelAdmin):
    list_display = ('stadium', 'caption')
    list_filter = ('stadium',)