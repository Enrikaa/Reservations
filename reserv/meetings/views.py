from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Reservation, MeetingRoom, Employee
from .serializers import (
    ReservationSerializer,
    MeetingRoomSerializer,
    EmployeeSerializer,
)
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, generics, mixins
from rest_framework.views import APIView
import numpy as np

# Make filter by status
class GetRooms(generics.ListAPIView):
    serializer_class = MeetingRoomSerializer
    queryset = MeetingRoom.objects.all()


class GetUsers(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


# --- Atspausdinti laisvus room's /rooms urle
# Make filter by status
class GetReservations(generics.ListAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    print("0")
    # print(request.data)


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
