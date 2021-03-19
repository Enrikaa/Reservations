from rest_framework import serializers
from .models import MeetingRoom, Reservation, User
from djoser.serializers import UserCreateSerializer, UserSerializer


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


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"


class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = "__all__"
