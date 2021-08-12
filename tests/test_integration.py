from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from meetings.models import User
from meetings.utils.test_utils import BaseTestCase


class TestUsers(BaseTestCase):

    def test_can_create_user(self):
        data = {"email": 'enrika1@gmail.com',
                "username": 'enrika1',
                "password": 'enr',
                "first_name": 'enrika1',
                "last_name": 'enrika1',
                "is_staff": True,
                }
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse("users-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_users(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestReservations(BaseTestCase):

    def test_all_get_reservations(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("reservations-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_reservation(self):
        data = {"title": "Title123",
                "date_from": "2021-03-18T08:40:36Z",
                "date_to": "2021-03-19T09:40:38Z",
                "organizer": self.user.id,
                "users": [self.user.id],
                "room": self.room.id,
                "external": False
                }
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse("reservations-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_reservation_with_to_many_users(self):
        fake_user_1 = baker.make(User, _create_files=True)
        fake_user_2 = baker.make(User, _create_files=True)
        fake_user_3 = baker.make(User, _create_files=True)
        data = {"title": "Title123",
                "date_from": "2021-03-18T08:40:36Z",
                "date_to": "2021-03-19T09:40:38Z",
                "organizer": self.user.id,
                "users": [self.user.id, fake_user_1.id, fake_user_2.id, fake_user_3.id],
                "room": self.room.id,
                "external": False
                }
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse("reservations-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {'non_field_error': ['to_many_users_in_room']})

    def test_create_reservation_with_bad_title(self):
        data = {"title": "",
                "date_from": "2021-03-18T08:40:36Z",
                "date_to": "2021-03-19T09:40:38Z",
                "organizer": self.user.id,
                "room": self.room.id,
                "users": [self.user.id],
                "external": False,
                "foo": "Bar"
                }
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse("reservations-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {'title': ['This field may not be blank.', ]})

    def test_create_reservation_past(self):
        data = {"title": "Title123",
                "date_from": "2020-03-18T08:40:36Z",
                "date_to": "2020-03-19T09:40:38Z",
                "organizer": self.user.id,
                "room": self.room.id,
                "users": [self.user.id],
                "external": False
                }
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse("reservations-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_delete_reservation(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(
            f"/api/v1/reservation/delete/{self.reservation.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_reservation_with_time_which_is_in_the_middle_of_existing_time(self):
        """
        In test database there is room with this time:
        date_from = "2021-08-07T19:57:01.615Z"
        date_to = "2021-08-20T19:57:01.615Z"
        """
        date_from = "2021-08-08T19:57:01.615Z"
        date_to = "2021-08-19T19:57:01.615Z"
        data = {"title": "Title123",
                "date_from": date_from,
                "date_to": date_to,
                "organizer": self.user.id,
                "room": self.room.id,
                "users": [self.user.id],
                "external": False
                }

        self.client.force_authenticate(self.user)
        response = self.client.post(reverse("reservations-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(response.json(), {'non_field_error': ['reservation_cancelled_with_wrong_time']})

    def test_create_reservation_with_time_which_is_equal_with_existing_time(self):
        """
        In test database there is room with this time:
        date_from = "2021-08-07T19:57:01.615Z"
        date_to = "2021-08-20T19:57:01.615Z"
        """
        date_from = "2021-08-07T19:57:01.615Z"
        date_to = "2021-08-20T19:57:01.615Z"

        data = {"title": "Title123",
                "date_from": date_from,
                "date_to": date_to,
                "organizer": self.user.id,
                "room": self.room.id,
                "users": [self.user.id],
                "external": False
                }

        self.client.force_authenticate(self.user)
        response = self.client.post(reverse("reservations-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(response.json(), {'non_field_error': ['reservation_cancelled_with_wrong_time']})

    def test_create_reservation_with_one_minute_after_previous_reservation_ended(self):
        """
        In test database there is room with this time:
        date_from = "2021-08-07T19:57:01.615Z"
        date_to = "2021-08-20T19:57:01.615Z"
        """
        date_from = "2021-10-20T19:59:01.615Z"
        date_to = "2022-10-25T19:57:01.615Z"
        data = {
            "title": "Title123",
            "date_from": date_from,
            "date_to": date_to,
            "organizer": self.user.id,
            "room": self.room.id,
            "users": [self.user.id],
            "external": False
        }

        self.client.force_authenticate(self.user)
        response = self.client.post(reverse("reservations-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    def test_create_reservation_which_wraps_the_existing_reservation_time(self):
        """
        In test database there is room with this time:
        date_from = "2021-08-07T19:57:01.615Z"
        date_to = "2021-08-20T19:57:01.615Z"
        """
        date_from = "2021-08-06T19:57:01.615Z"
        date_to = "2021-08-21T19:57:01.615Z"

        data = {"title": "Title123",
                "date_from": date_from,
                "date_to": date_to,
                "organizer": self.user.id,
                "room": self.room.id,
                "users": [self.user.id],
                "external": False
                }

        self.client.force_authenticate(self.user)
        response = self.client.post(reverse("reservations-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(response.json(), {'non_field_error': ['reservation_cancelled_with_wrong_time']})

    def test_create_reservation_with_time_which_wraps_existing_reservation_date_to_time(self):
        """
        In test database there is room with this time:
        date_from: 2021-08-07T19:57:01.615Z
        date_out: 2021-08-20T19:57:01.615Z
        """

        date_from = "2021-08-20T19:57:01.615Z"
        date_to = "2021-08-25T19:57:01.615Z"

        data = {
            "title": "Title123",
            "date_from": date_from,
            "date_to": date_to,
            "organizer": self.user.id,
            "room": self.room.id,
            "users": [self.user.id],
            "external": False
        }

        self.client.force_authenticate(self.user)
        response = self.client.post(reverse("reservations-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(response.json(), {'non_field_error': ['reservation_cancelled_with_wrong_time']})


class TestRooms(BaseTestCase):

    def test_get_rooms(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("rooms-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_rooms_ordering(self):
        self.client.force_authenticate(self.user)
        response = self.client.get("http://0.0.0.0:8000/api/v1/rooms/?ordering=title")  # minus
        results = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(results[0]['title'], "A")
        self.assertEqual(results[1]['title'], "B")
        self.assertEqual(results[2]['title'], "C")

    def test_get_rooms_filter(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse('rooms-list') + '?capacity=56')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()
        self.assertEqual(results[0]['capacity'], self.room.capacity)
        self.assertEqual(results[1]['capacity'], self.room3.capacity)
        self.assertEqual(len(results), 2)

    def test_get_rooms_search(self):
        self.client.force_authenticate(self.user)
        response = self.client.get("http://0.0.0.0:8000/api/v1/rooms/?search=DescriptionTesting")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()
        self.assertEqual(results[0]['id'], self.room.id)
        self.assertEqual(len(results), 1)


class TestAuthToken(BaseTestCase):

    def test_get_auth_token(self):
        data = {"email": self.email,
                "password": self.password}
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse("token_obtain_pair"), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_get_auth_wrong_token(self):
        data = {"email": 'a',
                "password": 'b'}
        self.client.force_authenticate(self.user)

        response = self.client.post(reverse("token_obtain_pair"), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json(), {'detail': 'No active account found with the given credentials'})
