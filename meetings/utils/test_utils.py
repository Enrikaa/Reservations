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
        self.user2 = User.objects.create_user(email='user2@gmail.com', username='user2', password=self.password,
                                              first_name='user2', last_name='user2',
                                              is_staff=self.is_staff
                                              )

        self.room = baker.make(MeetingRoom, title='A', capacity="56",
                               description="DescriptionTesting")  # search daromas pagal contains
        self.room3 = baker.make(MeetingRoom, title='C', capacity="56")
        self.room2 = baker.make(MeetingRoom, title='B')
        self.room4 = MeetingRoom.objects.create(title='Title', description='description', capacity='capacity',
                                                room_number="number")
        date_from = "2021-08-07T19:57:01.615Z"
        date_to = "2021-08-20T19:57:01.615Z"
        self.reservation = baker.make(Reservation, title='reservation', organizer=self.user, room=self.room,
                                      users=[self.user],
                                      date_from=date_from, date_to=date_to)
        self.reservation2 = baker.make(Reservation, title='reservation2', organizer=self.user2, room=self.room4,
                                       users=[self.user2],
                                       date_from=date_from, date_to=date_to)
        self.reservation3 = baker.make(Reservation, title='reservation3', organizer=self.user2, room=self.room4,
                                       users=[self.user],
                                       date_from=date_from, date_to=date_to)
