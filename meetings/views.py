from django.utils import timezone
import datetime
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from .models import Reservation, MeetingRoom
from .serializers import (
    ReservationSerializer,
    MeetingRoomSerializer,
)


# Get all rooms
class RoomsAll(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        room = MeetingRoom.objects.all()

        all_rooms = MeetingRoomSerializer(room, many=True)
        return Response(data=all_rooms.data)


# Get all reservations
class ReservationsAll(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()


# Get meeting room reservations
class ReservationByRoom(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, room_id):
        try:
            return MeetingRoom.objects.get(id=room_id)
        except MeetingRoom.DoesNotExist:
            raise NotFound(f"The meeting room id: {room_id} was not found.")

    # Get specific meeting room reservations
    def get(self, request, room_id):
        room = self.get_object(room_id=room_id)
        # Additional factor: setting to not show past reservations
        reservations = room.reservations.filter(date_from__gte=timezone.now())

        all_reservations = ReservationSerializer(reservations, many=True)
        return Response(data=all_reservations.data)


# Create reservation
class CreateReservation(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationSerializer

    def post(self, request):
        reservation_object = Reservation.objects.all()
        cut_reservations_strings = []

        for i in reservation_object:
            cut_reservations_strings.append(str((i.date_from))[0:16])
        request_data = request.data["date_from"][0:16]

        if request_data in cut_reservations_strings:
            raise NotFound(f"Can't create RESERVATION")
        else:
            return self.create(request)


# Check reservation by id and delete it
class DeleteReservation(APIView):
    permission_classes = [IsAuthenticated]

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
