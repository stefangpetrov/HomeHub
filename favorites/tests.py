from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from properties.models import Property

from .models import Favorite


class FavoriteModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="favoriteuser",
            password="testpass123"
        )

        self.property = Property.objects.create(
            title="Favorite Property",
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

    def test_favorite_is_connected_to_user_and_property(self):
        favorite = Favorite.objects.create(
            user=self.user,
            property=self.property
        )

        self.assertEqual(favorite.user, self.user)
        self.assertEqual(favorite.property, self.property)

    def test_user_cannot_favorite_same_property_twice(self):
        Favorite.objects.create(
            user=self.user,
            property=self.property
        )

        with self.assertRaises(IntegrityError):
            Favorite.objects.create(
                user=self.user,
                property=self.property
            )

class FavoriteViewsTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="viewfavoriteuser",
            password="testpass123"
        )

        self.property = Property.objects.create(
            title="Favorite View Property",
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

        self.client.login(
            username="viewfavoriteuser",
            password="testpass123"
        )

    def test_user_can_add_property_to_favorites(self):
        response = self.client.post(
            reverse("toggle_favorite", args=[self.property.pk])
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Favorite.objects.filter(
                user=self.user,
                property=self.property
            ).exists()
        )

    def test_user_can_remove_property_from_favorites(self):
        Favorite.objects.create(
            user=self.user,
            property=self.property
        )

        response = self.client.post(
            reverse("toggle_favorite", args=[self.property.pk])
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Favorite.objects.filter(
                user=self.user,
                property=self.property
            ).exists()
        )

    def test_user_can_view_favorites_list(self):
        Favorite.objects.create(
            user=self.user,
            property=self.property
        )

        response = self.client.get(
            reverse("favorite_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.property.title)