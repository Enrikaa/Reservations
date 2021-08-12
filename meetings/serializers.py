from django.core.exceptions import ValidationError
from django.db import transaction, connection
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

    def validate(self, validated_data):
        organizer = validated_data['organizer']
        user_reservation_count = Reservation.objects.select_related('organizer').filter(
            organizer=organizer)  # How many reservations have user

        users_with_superuser_status = User.objects.prefetch_related(
            'users_reservations').filter(is_staff=True)  # Admin with all privilegies should be lees than 10

        if len(user_reservation_count) >= 100:
            raise ValidationError(
                {'error': f'{organizer} user_have_to_many_reservations'},
            )

        if len(validated_data['users']) >= 4:
            raise ValidationError(
                {'non_field_error': 'to_many_users_in_room'},
            )

        if len(users_with_superuser_status) >= 10:
            raise ValidationError(
                {'is_staff': 'to_many_users_with_superuser_status'},
            )

        room = validated_data['room']
        check_in = validated_data['date_from']
        check_out = validated_data['date_to']

        check_room_time = Reservation.objects.filter(
            Q(room=room),
            Q(date_from__lte=check_in, date_to__gte=check_in) |
            Q(date_from__lte=check_out, date_to__gte=check_out) |
            Q(date_from__gte=check_in, date_to__lte=check_out)
        ).exists()

        if check_room_time:
            raise ValidationError(
                {'non_field_error': 'reservation_cancelled_with_wrong_time'}
            )
        return validated_data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.organizer:
            representation['organizer'] = instance.organizer.email
        return representation
