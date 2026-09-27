from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from properties.models import Property

from .models import Inquiry


class InquiryModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="inquiryuser",
            password="testpass123"
        )

        self.property = Property.objects.create(
            title="Inquiry Property",
            description="Test description",
            price=150000,
            area=80,
            bedrooms=2,
            bathrooms=1,
            floor=3,
            total_floors=6,
            city="Sofia",
            address="Test Address",
            owner=self.user,
            property_type=Property.PropertyType.APARTMENT,
            status=Property.Status.ACTIVE,
        )

    def test_inquiry_is_connected_to_user_and_property(self):
        inquiry = Inquiry.objects.create(
            user=self.user,
            property=self.property,
            message="I am interested in this property."
        )

        self.assertEqual(inquiry.user, self.user)
        self.assertEqual(inquiry.property, self.property)

    def test_inquiry_default_status_is_new(self):
        inquiry = Inquiry.objects.create(
            user=self.user,
            property=self.property,
            message="I am interested in this property."
        )

        self.assertEqual(inquiry.status, Inquiry.Status.NEW)

    def test_inquiry_str_contains_username_and_property_title(self):
        inquiry = Inquiry.objects.create(
            user=self.user,
            property=self.property,
            message="I am interested in this property."
        )

        self.assertEqual(
            str(inquiry),
            f"Inquiry from {self.user.username} - {self.property.title}"
        )

class InquiryViewsTest(TestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="buyer",
            password="testpass123",
            role=User.Role.USER,
        )

        self.agent = User.objects.create_user(
            username="agent",
            password="testpass123",
            role=User.Role.AGENT,
        )

        self.other_user = User.objects.create_user(
            username="otherbuyer",
            password="testpass123",
            role=User.Role.USER,
        )

        self.property = Property.objects.create(
            title="Inquiry Test Property",
            description="Test description",
            price=150000,
            area=80,
            bedrooms=2,
            bathrooms=1,
            floor=3,
            total_floors=6,
            city="Sofia",
            address="Test Address",
            owner=self.agent,
            property_type=Property.PropertyType.APARTMENT,
            status=Property.Status.ACTIVE,
        )

    def test_authenticated_user_can_create_inquiry(self):
        self.client.login(
            username="buyer",
            password="testpass123",
        )

        response = self.client.post(
            reverse("create_inquiry", args=[self.property.pk]),
            {
                "message": "I am interested in this property.",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Inquiry.objects.filter(
                user=self.user,
                property=self.property,
                message="I am interested in this property.",
            ).exists()
        )

    def test_anonymous_user_cannot_create_inquiry(self):
        response = self.client.get(
            reverse("create_inquiry", args=[self.property.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_agent_can_view_inquiries(self):
        inquiry = Inquiry.objects.create(
            user=self.user,
            property=self.property,
            message="Potential buyer",
        )

        self.client.login(
            username="agent",
            password="testpass123",
        )

        response = self.client.get(
            reverse("inquiry_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, inquiry.message)

    def test_agent_can_view_inquiries_for_owned_property(self):
        Inquiry.objects.create(
            user=self.user,
            property=self.property,
            message="Potential buyer",
        )

        self.client.login(
            username="agent",
            password="testpass123",
        )

        response = self.client.get(
            reverse("inquiry_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Potential buyer")