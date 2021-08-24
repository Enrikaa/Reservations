from django.db import connection, reset_queries
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from .models import MeetingRoom, Reservation, User
from .serializers import MeetingRoomSerializer, ReservationSerializer, \
    UsersSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'list']:
            self.permission_classes = [AllowAny, ]
        elif self.action in ['create']:
            self.permission_classes = [IsAuthenticated, ]
        print(len(connection.queries), "QUERIES COUNT")
        return super().get_permissions()

    def get_serializer_context(self):
        context = super(UserViewSet, self).get_serializer_context()
        context.update({'request': self.request.user})
        return context

    @action(detail=False, methods=["GET"])
    def user_created_reservations(self, request: Request, **kwargs) -> Response:
        """
        Finds reservations which is created by specific user
        """
        username = request.user.id
        reservations = Reservation.objects.select_related('organizer').filter(organizer=username)
        all_users = ReservationSerializer(reservations, many=True)
        return Response(data=all_users.data)

    @action(detail=False, methods=["GET"])
    def user_attending_reservations(self, request: Request, **kwargs) -> Response:
        """
        Finds attending reservations in which are specific user as a guest
        """
        username = request.user.id
        reservations = Reservation.objects.prefetch_related('users').filter(users=username)
        Reservation.objects.prefetch_related('users').filter(users=username)
        all_users = ReservationSerializer(reservations, many=True)
        return Response(data=all_users.data)


class RoomsAll(viewsets.ModelViewSet):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer
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
    def reservations(self, request: Request, **kwargs) -> Response:
        """
        Finds reservations by specific user id
        """
        room = self.get_object()
        reservations = room.reservations.filter(date_from__gte=timezone.now())
        all_reservations = ReservationSerializer(reservations, many=True)
        return Response(data=all_reservations.data)


class ReservationsAll(viewsets.ModelViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer: ReservationSerializer):
        serializer.save(organizer=self.request.user)
