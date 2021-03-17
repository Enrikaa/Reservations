from django.urls import path, include
from meetings import views
from .views import  GenericAPIView, GetReservations, RoomView

urlpatterns = [
    path("check/reservations/", GetReservations.as_view()),
    path("check/rooms/<int:room_id>/", RoomView.as_view()),
    path("check/room/<int:id>/", GenericAPIView.as_view()),
    path("", include("djoser.urls")),
    path("", include("djoser.urls.authtoken")),
    path("restricted/", views.restricted),
]
