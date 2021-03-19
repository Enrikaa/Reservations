from django.test import TestCase, Client
from meetings.models import User


class TestLogin(TestCase):
    def setUp(self):
        self.username = "test@test.com"
        self.password = "12345"
        self.user = User.objects.create_user(
            email=self.username, username=self.username, password=self.password
        )
        self.client = Client()

        self.room_1 = ""
        self.room_1_reservation = ""

    def test_login_success(self):
        """ Test user can login  """
        login_data = {"email": self.username, "password": self.password}
        response = self.client.post("/api/v1/meetings/token/login/", login_data)
        assert response.status_code == 200

    def test_wrong_credentials_unable_login(self):
        """  """
        login_data = {"email": "non_existing@gmail.com", "password": "wrong_pass"}
        response = self.client.post("/api/v1/meetings/token/login/", login_data)
        assert response.status_code == 400
        # If 200
        # response = self.client.get('')
        # response.content

    def test_can_cancel_reservation(self):
        """ Test if you can cancel existing reservation """
        reservation_id = self.room_1_reservation.id
        # send API request to cancel reservation
        # asert reservation does not exist in database

        # RoomReservation.objects.get(id=reservation_id)