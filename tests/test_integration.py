from django.test import TestCase
from rest_framework.test import APIClient
from meetings.models import Users, Reservation, MeetingRoom


class TestLogin(TestCase):

    last_name: str

    def setUp(self):

        self.email = "test@gmail.com"
        self.username = "Vysniaaaa"
        self.first_name = "Enrikaaaa"
        self.last_name = "Vyšniauskaitėe"
        self.password = "2051Enr2051Enre"
        self.re_password = "2051Enr2051Enre"
        self.client = APIClient()
        self.user = Users.objects.create_user(email=self.email, username=self.username,
                                              first_name=self.first_name, last_name=self.last_name, password=self.password)
        self.room_1 = MeetingRoom.objects.create(
            title="Room", description="Room 12", room_number="2", capacity="25")

    def test_get_auth_token(self):
        """ Test user can login """
        login_data = {"email": self.email,
                      "password": self.password}

        response = self.client.post("/api/v1/token/login/", login_data)
        assert response.status_code == 200
        self.assertTrue(response.json().get("auth_token", False))

    def test_create_reservation(self):
        """ Test or reservation create succesfuly"""
        reservation_data = {"title": "Title123",
                            "date_from": "2021-03-18T08:40:36Z",
                            "date_to": "2021-03-19T09:40:38Z",
                            "organizer": self.user.id,
                            "employees": [self.user.id],
                            "room": self.room_1.id
                            }
        self.client.force_authenticate(self.user)
        response = self.client.post(
            '/api/v1/create/reservation/', data=reservation_data)
        assert response.status_code == 201

    def test_wrong_credentials_unable_login(self):
        """ Test wrong credentials """
        login_data = {"email": "non_existing@gmail.com",
                      "password": "wrong_pass"}
        response = self.client.post(
            "/api/v1/token/login/", login_data)
        assert response.status_code == 400

    def test_can_cancel_reservation(self):
        """ Test if you can cancel existing reservation """

        reservation = Reservation.objects.create(
            title="TEST9",
            date_from="2050-03-18T07:40:36Z",
            date_to="2060-03-18T07:40:36Z",
            organizer=self.user,
            room=self.room_1,
        )
        self.client.force_authenticate(self.user)
        response = self.client.delete(
            f"/api/v1/reservation/delete/{reservation.id}/")
        assert response.status_code == 204
        self.assertFalse(Reservation.objects.filter(
            id=reservation.id).exists())

    def test_get_meeting_room_reservations(self):
        """ Test getting meeting room reservations """
        reservation = Reservation.objects.create(
            title="TEST9",
            date_from="2050-03-18T07:40:36Z",
            date_to="2060-03-18T07:40:36Z",
            organizer=self.user,
            room=self.room_1,
        )
        self.client.force_authenticate(self.user)
        response = self.client.get(
            f"/api/v1/reservations/room/{self.room_1.id}/")

        assert response.status_code == 200
        response_body = response.json()
        self.assertTrue(len(response_body) > 0)
