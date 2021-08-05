from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from .serializers import MeetingRoomSerializer, ReservationSerializer, \
    UsersSerializer
from .models import MeetingRoom, Reservation, User
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'list']:
            self.permission_classes = [AllowAny, ]
        elif self.action in ['create']:
            self.permission_classes = [IsAuthenticated, ]
        return super().get_permissions()

    def get_serializer_context(self):
        context = super(UserViewSet, self).get_serializer_context()
        context.update({'request': self.request.user})
        return context


class RoomsAll(viewsets.ModelViewSet):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['capacity']
    ordering_fields = ['title']
    search_fields = ['description']

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'list']:
            self.permission_classes = [AllowAny, ]
        elif self.action in ['create']:
            self.permission_classes = [IsAuthenticated, ]
        return super().get_permissions()

    @action(detail=True, methods=["GET"], throttle_classes=[UserRateThrottle])
    def reservations(self, request, **kwargs):
        room = self.get_object()
        reservations = room.reservations.filter(date_from__gte=timezone.now())
        print(reservations)
        all_reservations = ReservationSerializer(reservations, many=True)
        return Response(data=all_reservations.data)


class ReservationsAll(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        request_data = request.data, 'request'
        room_id = request_data[0]['room']
        room = MeetingRoom.objects.get(pk=room_id)
        check_in = request_data[0]['date_from']
        check_out = request_data[0]['date_to']
        case_1 = Reservation.objects.filter(room=room, date_from__lte=check_in, date_to__gte=check_in).exists()
        case_2 = Reservation.objects.filter(room=room, date_from__lte=check_out, date_to__gte=check_out).exists()
        case_3 = Reservation.objects.filter(room=room, date_from__gte=check_in, date_to__lte=check_out).exists()
        # if either of these is true, abort and render the error
        if case_1 or case_2 or case_3:
            raise ValidationError({'error': 'reservation_cancelled_with_wrong_time'})
        return super().create(request)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def example_adhoc_method(request, pk=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)
