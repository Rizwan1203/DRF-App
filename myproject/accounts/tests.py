import factory
from django.contrib.auth.models import User
from django.urls import reverse
from factory.django import DjangoModelFactory
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "testpassword")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")


class AuthenticationAPITestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

    def test_user_registration(self):
        user_data = {
            "username": "newuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
        }

        url = reverse("user-registration")
        response = self.client.post(url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_me(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        url = reverse("user-me")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": self.user.id,
                "username": self.user.username,
                "email": self.user.email,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
            },
        )

    def test_me_with_unauthenticated_user(self):
        url = reverse("user-me")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_obtain_token_view(self):
        url = reverse("create-token")
        data = {"username": self.user.username, "password": "testpassword"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_user_registration_with_mismatched_passwords(self):
        user_data = {
            "username": "testuser2",
            "password1": "testpassword",
            "password2": "mismatchedpassword",
            "email": "test2@example.com",
            "first_name": "Test",
            "last_name": "User2",
        }
        url = reverse("user-registration")
        response = self.client.post(url, user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_user_registration_with_existing_username(self):
        user_data = {
            "username": self.user.username,
            "password1": "testpassword",
            "password2": "testpassword",
            "email": "test3@example.com",
            "first_name": "Test",
            "last_name": "User3",
        }
        url = reverse("user-registration")
        response = self.client.post(url, user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
