from rest_framework import serializers
from .models import Employee, MeetingRoom, Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
        # read_only_fields = ("id",)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
        # read_only_fields = ("id",)


class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = "__all__"
        # read_only_fields = ("id",)


# class RoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Room
#         # fields = ["id", "title", "author", "email"]
#         fields = "__all__"


# class ReservationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Reservation
#         # fields = ["id", "title", "author", "email"]
#         fields = "__all__"
