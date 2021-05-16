# from django.test import TestCase
# from model_bakery import baker
# from rest_framework.test import APIClient
# from meetings.models import User, Reservation, MeetingRoom
# from django.urls import reverse
# from rest_framework import status
#
#
# class TestLogin(TestCase):
#     last_name: str
#
#     def setUp(self):
#         self.email = "admin@admin.com"
#         self.username = "testusername"
#         self.first_name = "testfirstname"
#         self.last_name = "testlastname"
#         self.password = "admin"
#         self.re_password = "testpassword"
#         self.is_staff = True
#         self.client = APIClient()
#         self.user = User.objects.create_user(email=self.email, username=self.username, password=self.password,
#                                              first_name=self.first_name, last_name=self.last_name,
#                                              is_staff=self.is_staff
#                                              )
#         self.room = baker.make(MeetingRoom)
#
#         # self.room = MeetingRoom.objects.create(
#         #     title="Room", description="Room 12", room_number="2", capacity="25")
#         # self.reservations = Reservation.objects.create(
#         #     title="Reservation", organizer=self.user.id, room=self.room.id, external=True, created_by="admin@admin.com",
#         #     date_from="2023-05-13T19:39:34Z", date_to="2023-06-13T19:39:36Z")
#
#     def test_can_create_user(self):
#         data = {"email": 'enrika1@gmail.com',
#                 "username": 'enrika1',
#                 "password": 'enr',
#                 "first_name": 'enrika1',
#                 "last_name": 'enrika1',
#                 "is_staff": True,
#                 }
#         self.client.force_authenticate(self.user)
#         response = self.client.post(reverse("users-list"), data=data)
#         print(response.json())
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#     def test_get_users(self):
#         self.client.force_authenticate(self.user)
#         response = self.client.get(reverse("users-list"))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_create_reservation(self):
#         data = {"title": "Title123",
#                 "date_from": "2021-03-18T08:40:36Z",
#                 "date_to": "2021-03-19T09:40:38Z",
#                 "organizer": self.user.id,
#                 "room": self.room.id,
#                 "external": False
#                 }
#         self.client.force_authenticate(self.user)
#         response = self.client.post(reverse("reservations-list"), data=data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#     def test_create_reservation_with_bad_title(self):
#         data = {"title": "",
#                 "date_from": "2021-03-18T08:40:36Z",
#                 "date_to": "2021-03-19T09:40:38Z",
#                 "organizer": self.user.id,
#                 "room": self.room.id,
#                 "external": False
#                 }
#         self.client.force_authenticate(self.user)
#         response = self.client.post(reverse("reservations-list"), data=data)
#         print(response.data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(
#             response.json(), {'title': ['This field may not be blank.', ]})
#

#
#     def test_get_reservations(self):
#         self.client.force_authenticate(self.user)
#         response = self.client.get(reverse("reservations-list"))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_get_auth_token(self):
#         data = {"email": self.email,
#                 "password": self.password}
#         self.client.force_authenticate(self.user)
#         response = self.client.post(reverse("token_obtain_pair"), data=data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.json()), 2)
#
#
#
#

#     # def test_can_cancel_reservation(self):
#     #     """ Test if you can cancel existing reservation """
#     #
#     #     reservation = Reservation.objects.create(
#     #         title="TEST9",
#     #         date_from="2050-03-18T07:40:36Z",
#     #         date_to="2060-03-18T07:40:36Z",
#     #         organizer=self.user,
#     #         room=self.room_1,
#     #     )
#     #     self.client.force_authenticate(self.user)
#     #     response = self.client.delete(
#     #         f"/api/v1/reservation/delete/{reservation.id}/")
#     #     assert response.status_code == 204
#     #     self.assertFalse(Reservation.objects.filter(
#     #         id=reservation.id).exists())
#     #
#     # def test_get_meeting_room_reservations(self):
#     #     """ Test getting meeting room reservations """
#     #     reservation = Reservation.objects.create(
#     #         title="TEST9",
#     #         date_from="2050-03-18T07:40:36Z",
#     #         date_to="2060-03-18T07:40:36Z",
#     #         organizer=self.user,
#     #         room=self.room_1,
#     #     )
#     #     self.client.force_authenticate(self.user)
#     #     response = self.client.get(
#     #         f"/api/v1/reservations/room/{self.room_1.id}/")
#     #
#     #     assert response.status_code == 200
#     #     response_body = response.json()
#     #     self.assertTrue(len(response_body) > 0)
