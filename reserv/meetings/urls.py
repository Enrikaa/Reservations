from django.urls import path, include
from meetings import views
from .views import *

urlpatterns = [

    # Authentication
    path("", include("djoser.urls")),
    path("", include("djoser.urls.authtoken")),
    # Create superuser
    path("users/", include("djoser.urls")),
    # Check if user is authentication
    path("authentication/checker/", restricted),


    # Check all rooms
    path("rooms/all/", RoomsAll.as_view()),
    # Check all reservations details
    path("reservations/all/", ReservationsAll.as_view()),
    # Check one reservation details
    path("reservation/<int:reservation_id>/", DeleteReservation.as_view()),
    # Delete reservation
    path("reservation/delete/<int:reservation_id>/", DeleteReservation.as_view()),
    # Reservations by room id
    path("reservations/room/<int:room_id>/", ReservationByRoom.as_view()),
    # Create reservation
    path("create/reservation/", CreateReservation.as_view()),

]
