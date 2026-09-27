from django.test import TestCase
from django.urls import reverse


from .models import User


class UserModelTest(TestCase):

    def test_user_default_role_is_user(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        self.assertEqual(user.role, User.Role.USER)

    def test_user_can_have_agent_role(self):
        user = User.objects.create_user(
            username="agentuser",
            password="testpass123",
            role=User.Role.AGENT
        )

        self.assertEqual(user.role, User.Role.AGENT)

    def test_user_can_have_admin_role(self):
        user = User.objects.create_user(
            username="adminuser",
            password="testpass123",
            role=User.Role.ADMIN
        )

        self.assertEqual(user.role, User.Role.ADMIN)

    def test_user_str_returns_username(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        self.assertEqual(str(user), "testuser")


class UserViewsTest(TestCase):

    def test_register_view_creates_user(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "first_name": "New",
                "last_name": "User",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            User.objects.filter(username="newuser").exists()
        )

    def test_login_view_logs_user_in(self):
        User.objects.create_user(
            username="loginuser",
            password="StrongPass123!"
        )

        response = self.client.post(
            reverse("login"),
            {
                "username": "loginuser",
                "password": "StrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            int(self.client.session["_auth_user_id"]),
            User.objects.get(username="loginuser").pk
        )

    def test_login_view_rejects_invalid_password(self):
        User.objects.create_user(
            username="loginuser",
            password="StrongPass123!"
        )

        response = self.client.post(
            reverse("login"),
            {
                "username": "loginuser",
                "password": "WrongPassword123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)