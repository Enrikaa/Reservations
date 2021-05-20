from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
        read_only_fields = ('created_by',)


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id",
                  "title",
                  "organizer",
                  "room",
                  "external",
                  "created_by",
                  "date_from",
                  "date_to",
                  ]
        read_only_fields = ('created_by',)

    def validate_title(self, data):
        if 'title' == '':
            raise ValidationError(
                {'password': 'password_no_upper'},
            )
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.created_by:
            representation['created_by'] = instance.created_by.email

        return representation
