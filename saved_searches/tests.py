from django.contrib.auth import get_user_model
from django.test import TestCase

from properties.models import Property

from .models import Notification, SavedSearch

from .services import check_saved_searches


class SavedSearchModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="searchuser",
            password="testpass123"
        )

        self.property = Property.objects.create(
            title="Search Property",
            description="Test description",
            price=200000,
            area=90,
            bedrooms=3,
            bathrooms=2,
            floor=4,
            total_floors=8,
            city="Sofia",
            address="Test Address",
            owner=self.user,
            property_type=Property.PropertyType.APARTMENT,
            status=Property.Status.ACTIVE,
        )

    def test_saved_search_is_connected_to_user(self):
        saved_search = SavedSearch.objects.create(
            user=self.user,
            name="My Sofia Search",
            city="Sofia",
            min_price=150000,
            max_price=250000,
            min_bedrooms=2,
        )

        self.assertEqual(saved_search.user, self.user)

    def test_saved_search_str_contains_name_and_username(self):
        saved_search = SavedSearch.objects.create(
            user=self.user,
            name="My Sofia Search",
        )

        self.assertEqual(
            str(saved_search),
            f"{saved_search.name} - {self.user.username}"
        )


class NotificationModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="notificationuser",
            password="testpass123"
        )

        self.property = Property.objects.create(
            title="Notification Property",
            description="Test description",
            price=200000,
            area=90,
            bedrooms=3,
            bathrooms=2,
            floor=4,
            total_floors=8,
            city="Sofia",
            address="Test Address",
            owner=self.user,
            property_type=Property.PropertyType.APARTMENT,
            status=Property.Status.ACTIVE,
        )

        self.saved_search = SavedSearch.objects.create(
            user=self.user,
            name="My Search",
            city="Sofia",
        )

    def test_notification_is_connected_to_user_property_and_saved_search(self):
        notification = Notification.objects.create(
            user=self.user,
            property=self.property,
            saved_search=self.saved_search,
            message="New property matches your saved search.",
        )

        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.property, self.property)
        self.assertEqual(notification.saved_search, self.saved_search)

    def test_notification_is_unread_by_default(self):
        notification = Notification.objects.create(
            user=self.user,
            property=self.property,
            saved_search=self.saved_search,
            message="New property matches your saved search.",
        )

        self.assertFalse(notification.is_read)

class SavedSearchServiceTest(TestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="serviceuser",
            password="testpass123",
        )

        self.owner = User.objects.create_user(
            username="owner",
            password="testpass123",
            role=User.Role.AGENT,
        )

        self.saved_search = SavedSearch.objects.create(
            user=self.user,
            name="Sofia Apartments",
            city="Sofia",
            property_type=Property.PropertyType.APARTMENT,
            min_price=100000,
            max_price=250000,
            min_bedrooms=2,
        )

    def create_property(self, **overrides):
        data = {
            "title": "Matching Apartment",
            "description": "Test description",
            "price": 200000,
            "area": 90,
            "bedrooms": 3,
            "bathrooms": 2,
            "floor": 4,
            "total_floors": 8,
            "city": "Sofia",
            "address": "Test Address",
            "owner": self.owner,
            "property_type": Property.PropertyType.APARTMENT,
            "status": Property.Status.ACTIVE,
        }

        data.update(overrides)

        return Property.objects.create(**data)

    def test_matching_property_creates_notification(self):
        property = self.create_property()

        check_saved_searches(property)

        self.assertTrue(
            Notification.objects.filter(
                user=self.user,
                property=property,
                saved_search=self.saved_search,
            ).exists()
        )

    def test_non_matching_property_does_not_create_notification(self):
        property = self.create_property(
            city="Plovdiv",
        )

        check_saved_searches(property)

        self.assertFalse(
            Notification.objects.filter(
                user=self.user,
                property=property,
                saved_search=self.saved_search,
            ).exists()
        )