from django.urls import path
from . import views

urlpatterns = [
    path("stadiums/", views.stadium_list, name="stadium_list"),
    path("stadiums/<int:stadium_id>/", views.stadium_detail, name="stadium_detail"),
    path("fields/<int:field_id>/schedule/", views.field_schedule, name="field_schedule"),
    path("fields/<int:field_id>/edit/", views.edit_field, name="edit_field"),
    path("fields/<int:field_id>/book/", views.create_booking, name="create_booking"),
    path("bookings/<int:booking_id>/action/", views.booking_action, name="booking_action"),
    path("fields/<int:field_id>/maintenance/add/", views.add_maintenance, name="add_maintenance"),
    path("maintenance/<int:booking_id>/edit/", views.edit_maintenance, name="edit_maintenance"),
    path("maintenance/<int:booking_id>/delete/", views.delete_maintenance, name="delete_maintenance"),
]