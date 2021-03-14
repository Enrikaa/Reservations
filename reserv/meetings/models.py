from django.db import models
from django.contrib.auth.models import User
import uuid

uuid.uuid4()


class Employee(models.Model):
    # employee_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)


class MeetingRoom(models.Model):
    # room_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    room_number = models.CharField(max_length=16, unique=True)


class Reservation(models.Model):
    STATUS_VALID = 0
    STATUS_CANCELLED = 1
    STATUS_TYPES = [
        (STATUS_VALID, "Valid"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    # meeting_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    room = models.ForeignKey(
        MeetingRoom, related_name="reservations", on_delete=models.CASCADE
    )
    organizer = models.ForeignKey(
        Employee, related_name="organized_reservations", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=150)
    status = models.IntegerField(choices=STATUS_TYPES, default=STATUS_VALID)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()


# class Room(models.Model):
#     name = models.CharField(max_length=100)
#     desc = models.TextField()
#     is_reserved = models.BooleanField(default=False)
#     capacity = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "Room"


# class Reservation(models.Model):
#     title = models.CharField(max_length=100)
#     check_in = models.DateTimeField()
#     check_out = models.DateTimeField()
#     registrant = models.ForeignKey(User, on_delete=models.CASCADE)
#     employees = models.ManyToManyField(User, related_name="participants")
#     external = models.BooleanField(default=False)
#     number_of_people = models.PositiveIntegerField()
#     status = models.CharField(
#         max_length=50, choices=(("0", "Valid"), ("1", "Cancelled"))
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title

#     class Meta:
#         verbose_name = "Reservation"


# room = models.ForeignKey(
#     Room, related_name="reservations", on_delete=models.CASCADE
# )  # backref to reservations
