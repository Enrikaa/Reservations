from django.contrib import admin
from .models import Employee, MeetingRoom, Reservation

admin.site.register(Employee)
admin.site.register(MeetingRoom)
admin.site.register(Reservation)


# @admin.register(Room)
# class RoomAdmin(admin.ModelAdmin):
#     list_display = ("id", "name")


# @admin.register(Reservation)
# class ReservationAdmin(admin.ModelAdmin):
#     list_display = ("id", "title", "status", "external")