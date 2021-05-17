from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MeetingRoomSerializer, ReservationSerializer, \
    UsersSerializer

from .models import MeetingRoom, Reservation, User
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'

    # def get_permissions(self):
    #     if self.action in ['update', 'partial_update', 'destroy', 'list']:
    #         self.permission_classes = [AllowAny, ]
    #     elif self.action in ['create']:
    #         self.permission_classes = [IsAuthenticated, ]
    #     return super().get_permissions()

    def get_serializer_context(self):
        context = super(UserViewSet, self).get_serializer_context()
        context.update({'request': 'request.data'})
        return context


class RoomsAll(viewsets.ModelViewSet):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['room_number']

    # def get_permissions(self):
    #     if self.action in ['update', 'partial_update', 'destroy', 'list']:
    #         self.permission_classes = [AllowAny, ]
    #     elif self.action in ['create']:
    #         self.permission_classes = [IsAuthenticated, ]
    #     return super().get_permissions()


class ReservationsAll(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    lookup_field = 'id'

    @action(detail=True, methods=["GET"])
    def rooms(self, request, id):
        room = MeetingRoom.objects.get(id=id)
        reservations = room.reservations.filter(date_from__gte=timezone.now())
        all_reservations = ReservationSerializer(reservations, many=True)
        print(all_reservations)
        return Response(data=all_reservations.data)

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


class DeleteReservation(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

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
