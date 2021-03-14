from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Reservation, MeetingRoom
from .serializers import ReservationSerializer, MeetingRoomSerializer
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, generics, mixins
from rest_framework.views import APIView

# Make filter by status
class GetRooms(generics.ListAPIView):
    serializer_class = MeetingRoomSerializer
    queryset = MeetingRoom.objects.all()


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
        return self.create(request, id)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)
