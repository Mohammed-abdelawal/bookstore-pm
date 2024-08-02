from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class RegisterAuthTests(APITestCase):

    def test_register_user(self):
        url = reverse("register")
        data = {
            "username": "Abdelawaal",
            "email": "abd.elawal@example.com",
            "password": "testpassw0rd",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "Abdelawal")

    def test_register_user_missing_fields(self):
        url = reverse("register")
        data = {"username": "Abdelawal"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginAuthTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="Mohammed", password="passw0rd")

    def test_login_user(self):
        url = reverse("token_obtain_pair")
        data = {"username": "Mohammed", "password": "passw0rd"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_user_invalid_credentials(self):
        url = reverse("token_obtain_pair")
        data = {"username": "Mohammed", "password": "wr0ng"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
