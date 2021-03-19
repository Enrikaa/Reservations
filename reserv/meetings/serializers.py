from rest_framework import serializers
from .models import MeetingRoom, Reservation, User
from djoser.serializers import UserCreateSerializer, UserSerializer


# User model serializer
class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            "id",
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
        )


# Reservation model serializer
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"


# MeetingRoom model serializer
class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = "__all__"
