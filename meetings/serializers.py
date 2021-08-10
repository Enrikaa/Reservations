from django.core.exceptions import ValidationError
from django.db import transaction
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
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            user.save()
        u = User.objects.select_related('auth_token').get(email=validated_data['email'])
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
                  "users",
                  "external",
                  "date_from",
                  "date_to",
                  ]

    def validate_users(self, data):
        print(len(data))
        if len(data) >= 4:
            raise ValidationError(
                {'error': 'to_many_users_in_room'},
            )
        return data

    def validate(self, data):
        room = data['room']
        check_in = data['date_from']
        check_out = data['date_to']

        check_room_time = Reservation.objects.filter(room=room).filter(
            Q(date_from__lte=check_in, date_to__gte=check_in) |
            Q(date_from__lte=check_out, date_to__gte=check_out) |
            Q(date_from__gte=check_in, date_to__lte=check_out)
        ).exists()

        if check_room_time:
            raise ValidationError(
                {'error': 'reservation_cancelled_with_wrong_time'}
            )
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.organizer:
            representation['organizer'] = instance.organizer.email
        return representation
