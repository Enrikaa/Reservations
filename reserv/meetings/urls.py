from django.urls import path, include
from .views import GetRooms, GenericAPIView, GetReservations, GetUsers

urlpatterns = [
    path("rooms/", GetRooms.as_view()),
    path("reservations/", GetReservations.as_view()),
    path("generic/room/<int:id>/", GenericAPIView.as_view()),
    path("getusers/", GetUsers.as_view()),
    path("", include("djoser.urls")),
    path("", include("djoser.urls.authtoken")),
]
