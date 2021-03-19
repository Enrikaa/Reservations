from django.db import models

# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Docker
class Post(models.Model):

    title = models.CharField(max_length=250)
    content = models.TextField()

    def __str__(self):
        return self.title


class User(AbstractUser):

    email = models.EmailField(verbose_name="email", max_length=255, unique=True)
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "password"]
    USERNAME_FIELD = "email"

    def get_username(self):
        return self.email


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
    employees = models.ManyToManyField(User)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()

    def __str__(self):
        return self.title
