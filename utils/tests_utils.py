from django.test import TestCase
from model_bakery import baker
from rest_framework.test import APIClient
from meetings.models import User, Reservation, MeetingRoom


class BaseTestCase(TestCase):

    def setUp(self):
        self.email = "admin@admin.com"
        self.username = "testusername"
        self.first_name = "testfirstname"
        self.last_name = "testlastname"
        self.password = "admin"
        self.re_password = "testpassword"
        self.is_staff = True
        self.client = APIClient()
        self.user = User.objects.create_user(email=self.email, username=self.username, password=self.password,
                                             first_name=self.first_name, last_name=self.last_name,
                                             is_staff=self.is_staff
                                             )
        self.room = baker.make(MeetingRoom)
        self.reservations = Reservation.objects.create(title="Reservation", organizer=self.user, room=self.room,
                                                       external=True,
                                                       date_from="2023-05-13T19:39:34Z", date_to="2023-06-13T19:39:36Z")
        self.user_wrong = baker.make(User)
