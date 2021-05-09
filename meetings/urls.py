from django.urls import include, path

from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView

from .views import DeleteReservation, ReservationByRoom, \
    ReservationsAll, RoomsAll, UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('rooms', RoomsAll)
router.register('reservations', ReservationsAll)
urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("reservation/delete/<int:reservation_id>/", DeleteReservation.as_view()),
    path("reservations/room/<int:room_id>/", ReservationByRoom.as_view()),

]