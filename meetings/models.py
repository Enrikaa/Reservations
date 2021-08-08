from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from meetings.utils.abstract_class import AbstractClass


class User(AbstractUser):
    email = models.EmailField(verbose_name="email",
                              max_length=255, unique=True)
    REQUIRED_FIELDS = ["username", "first_name", "password", "is_staff"]
    USERNAME_FIELD = "email"


class MeetingRoom(AbstractClass):
    title = models.CharField(max_length=150)
    description = models.TextField()
    room_number = models.CharField(max_length=16, unique=True)
    capacity = models.CharField(max_length=100)

    def __str__(self):
        return self.room_number


class Reservation(AbstractClass):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=300, blank=True)
    organizer = models.ForeignKey(
        User, related_name="organized_reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        MeetingRoom, related_name="reservations", on_delete=models.CASCADE
    )
    users = models.ManyToManyField(User, related_name="users_reservations")
    external = models.BooleanField(default=False)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()

    def __str__(self):
        return self.title
