from django.utils import timezone

from rest_framework import filters
from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MeetingRoomSerializer, ReservationSerializer, \
    UsersSerializer

from .models import MeetingRoom, Reservation, User


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UsersSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'list']:
            self.permission_classes = [AllowAny, ]
        elif self.action in ['create']:
            self.permission_classes = [IsAuthenticated, ]
        return super().get_permissions()


class RoomsAll(viewsets.ModelViewSet):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'list']:
            self.permission_classes = [AllowAny, ]
        elif self.action in ['create']:
            self.permission_classes = [IsAuthenticated, ]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ReservationsAll(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def post(self, request):
        reservation_object = Reservation.objects.all()
        cut_reservations_strings = []
        for i in reservation_object:
            cut_reservations_strings.append(str((i.date_from))[0:16])
        request_data = request.data["date_from"][0:16]
        if request_data in cut_reservations_strings:
            raise NotFound("Can't create RESERVATION")
        else:
            return self.create(request)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ReservationByRoom(APIView):

    def get_object(self, room_id):
        try:
            return MeetingRoom.objects.get(id=room_id)
        except MeetingRoom.DoesNotExist:
            raise NotFound(f"The meeting room id: {room_id} was not found.")

    def get(self, request, room_id):
        room = self.get_object(room_id=room_id)
        reservations = room.reservations.filter(date_from__gte=timezone.now())
        all_reservations = ReservationSerializer(reservations, many=True)
        return Response(data=all_reservations.data)


class DeleteReservation(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_reservation(self, reservation_id):
        try:
            return Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            raise NotFound(
                f"The reservation reservation id: {reservation_id} was not found."
            )

    def get(self, request, reservation_id):
        rooms = self.get_reservation(reservation_id=reservation_id)
        serializer = ReservationSerializer(rooms)
        return Response(serializer.data)

    def delete(self, request, reservation_id):
        reservation = self.get_reservation(reservation_id=reservation_id)
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
