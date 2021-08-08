from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import serializers

from .models import MeetingRoom, Reservation, User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "is_staff",
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user


class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id",
                  "title",
                  "organizer",
                  "room",
                  "external",
                  "date_from",
                  "date_to",
                  ]

    def validate_title(self, data):
        if 'title' == '':
            raise ValidationError(
                {'password': 'password_no_upper'},
            )
        return data

    def validate(self, data):
        room = data['room']
        check_in = data['date_from']
        check_out = data['date_to']

        case = Reservation.objects.filter(room=room).filter(
            Q(date_from__lte=check_in, date_to__gte=check_in) |
            Q(date_from__lte=check_out, date_to__gte=check_out) |
            Q(date_from__gte=check_in, date_to__lte=check_out)
        ).exists()

        if case:
            raise ValidationError(
                {'error': 'reservation_cancelled_with_wrong_time'}
            )
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.organizer:
            representation['organizer'] = instance.organizer.email

        return representation
