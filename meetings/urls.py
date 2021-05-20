from django.urls import include, path

from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView

from .views import ReservationsAll, RoomsAll, UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('rooms', RoomsAll, basename='rooms')
router.register('reservations', ReservationsAll, basename='reservations')
urlpatterns = router.urls

#

urlpatterns = [
    path('', include(router.urls)),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')

]
