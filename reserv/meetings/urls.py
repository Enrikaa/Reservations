from django.urls import path
from .views import GetRooms, GenericAPIView, GetReservations, GetUsers

urlpatterns = [
    path("rooms/", GetRooms.as_view()),
    path("reservations/", GetReservations.as_view()),
    path("generic/room/<int:id>/", GenericAPIView.as_view()),
    path("users/", GetUsers.as_view()),
]
