import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .models import Reservation, MeetingRoom
from .serializers import (
    ReservationSerializer,
    MeetingRoomSerializer,
)
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import (
    SessionAuthentication,
    TokenAuthentication,
    BasicAuthentication,
)
from rest_framework.exceptions import NotFound

# Check if user is authenticated


# Get all rooms
class RoomsAll(APIView):
    def get(self, request):
        room = MeetingRoom.objects.all()

        all_rooms = MeetingRoomSerializer(room, many=True)
        return Response(data=all_rooms.data)


# Get all reservations
class ReservationsAll(generics.ListAPIView):

    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()


# Get meeting room reservations
class ReservationByRoom(APIView):
    def get_object(self, room_id):
        try:
            return MeetingRoom.objects.get(id=room_id)
        except MeetingRoom.DoesNotExist:
            raise NotFound(f"The meeting room id: {room_id} was not found.")

    # Get specific meeting room reservations
    def get(self, request, room_id):
        room = self.get_object(room_id=room_id)
        reservations = room.reservations.filter(date_from__gte=timezone.now())

        all_reservations = ReservationSerializer(reservations, many=True)
        return Response(data=all_reservations.data)


class CreateReservation(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
):

    serializer_class = ReservationSerializer

    def post(self, request):
        return self.create(request)


# Check reservation by id and delete it
class DeleteReservation(APIView):
    def get_reservation(self, reservation_id):
        try:
            return Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            raise NotFound(
                f"The reservation reservation id: {reservation_id} was not found."
            )

    def get(self, request, reservation_id):
        # Take data from above function
        rooms = self.get_reservation(reservation_id=reservation_id)
        serializer = ReservationSerializer(rooms)
        return Response(serializer.data)

    def delete(self, request, reservation_id):
        reservation = self.get_reservation(reservation_id=reservation_id)
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
