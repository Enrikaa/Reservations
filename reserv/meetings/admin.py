from django.contrib import admin
from .models import Employee, MeetingRoom, Reservation

admin.site.register(Employee)
admin.site.register(MeetingRoom)
admin.site.register(Reservation)
