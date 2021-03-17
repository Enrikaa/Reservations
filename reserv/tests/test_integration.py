from django.test import TestCase, Client
from meetings.models import User

class TestLogin(TestCase):
    def setUp(self):
        self.username = "test@test.com"
        self.password = "12345"
        self.user = User.objects.create_user(email=self.username, username=self.username, password=self.password)
        self.client = Client()

    def test_login_success(self):
        """ Test user can login  """
        login_data = {
            "email": self.username,
            "password": self.password
        }
        response = self.client.post('/api/v1/meetings/token/login/', login_data)
        assert response.status_code == 200
    
    def test_wrong_credentials_unable_login(self):
        """  """
        login_data = {
            "email": "non_existing@gmail.com",
            "password": "wrong_pass"
        }
        response = self.client.post('/api/v1/meetings/token/login/', login_data)
        assert response.status_code == 400
        # If 200
        # response = self.client.get('')
        # response.content