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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def restricted(request, *args, **kwargs):
    return Response(
        data="Information just for logged in Users", status=status.HTTP_200_OK
    )


# Make filter by status
# class MeetingRoom(APIView):

#     def get_object(self, id):

#         try:
#             return MeetingRoom.objects.get(id=id)
#         except MeetingRoom.DoesNotExist:
#             return HttpResponse(status=status.HTTP_404_NOT_FOUND)

#         serializer_class = MeetingRoomSerializer
#         queryset = MeetingRoom.objects.all()


class RoomView(APIView):

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

    def post(self, request, room_id):
        post_body = json.loads(request.body)
        reservation_serializer = ReservationSerializer(data=post_body)

        if reservation_serializer.is_valid():
            reservation_serializer.save()
            return Response(data=reservation_serializer.data)
        else:
            return Response(data=reservation_serializer.errors)


# Make filter by status
class GetReservations(generics.ListAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()


class GenericAPIView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    lookup_field = "id"

    def get(self, request, id=None):

        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request, id=None):

        reservations = Reservation.objects.all()
        reservations_start_hour = []
        data = request.data

        post_start_hour = str(data["date_from"])
        start_time = post_start_hour[11:13]

        post_end_hour = str(data["date_to"])
        end_time = post_end_hour[11:13]

        for i in reservations:

            reservations_start_hour = str(i.date_from)
            start_hour = reservations_start_hour[11:13]

            reservations_end_hour = str(i.date_to)
            end_hour = reservations_end_hour[11:13]

            if int(start_hour) > int(start_time) and int(end_time) < int(start_hour):
                return self.create(request, id)
            elif int(start_hour) < int(start_time) and int(start_time) > int(end_hour):
                return self.create(request, id)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)
