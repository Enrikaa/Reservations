from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(verbose_name="email",
                              max_length=255, unique=True)
    REQUIRED_FIELDS = ["username", "first_name", "password", "is_staff"]
    USERNAME_FIELD = "email"


class MeetingRoom(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    room_number = models.CharField(max_length=16, unique=True)
    capacity = models.CharField(max_length=100)

    def __str__(self):
        return self.room_number


class Reservation(models.Model):
    title = models.CharField(max_length=150)
    organizer = models.ForeignKey(
        User, related_name="organized_reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        MeetingRoom, related_name="reservations", on_delete=models.CASCADE
    )
    external = models.BooleanField(default=False)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    created_by = models.ForeignKey(User, related_name='user_name',
                                   max_length=16, on_delete=models.CASCADE,
                                   null=True)

    def __str__(self):
        return self.title
