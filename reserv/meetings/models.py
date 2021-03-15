from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=255, unique=True)
    phone = models.CharField(null=True, max_length=255)
    REQUIRED_FIELDS = ["username", "phone", "first_name", "last_name"]
    USERNAME_FIELD = "email"

    def get_username(self):
        return self.email


class Employee(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    def __str__(self):
        return self.first_name


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
    employess_list = models.ManyToManyField(Employee, related_name="participants")
    external = models.BooleanField(default=False)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()

    def __str__(self):
        return self.title
