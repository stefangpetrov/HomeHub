from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Property, PropertyImage

from django.urls import reverse


class PropertyModelTest(TestCase):

    def test_floor_cannot_be_greater_than_total_floors(self):
        user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123"
        )

        property = Property(
            title="Test Property",
            description="Test description",
            price=100000,
            area=80,
            bedrooms=2,
            bathrooms=1,
            floor=7,
            total_floors=6,
            city="Sofia",
            address="Test Address",
            owner=user,
            property_type=Property.PropertyType.APARTMENT,
            status=Property.Status.ACTIVE,
        )

        with self.assertRaises(ValidationError):
            property.full_clean()


    def test_valid_floor_is_accepted(self):
        user = get_user_model().objects.create_user(
            username="validuser",
            password="testpass123"
        )

        property = Property(
            title="Valid Property",
            description="Test description",
            price=100000,
            area=80,
            bedrooms=2,
            bathrooms=1,
            floor=6,
            total_floors=6,
            city="Sofia",
            address="Test Address",
            owner=user,
            property_type=Property.PropertyType.APARTMENT,
            status=Property.Status.ACTIVE,
        )

        property.full_clean()

    def test_property_has_owner(self):
            user = get_user_model().objects.create_user(
                username="owneruser",
                password="testpass123"
            )
    
            property = Property.objects.create(
                title="Owned Property",
                description="Test description",
                price=100000,
                area=80,
                bedrooms=2,
                bathrooms=1,
                floor=3,
                total_floors=6,
                city="Sofia",
                address="Test Address",
                owner=user,
                property_type=Property.PropertyType.APARTMENT,
                status=Property.Status.ACTIVE,
            )
    
            self.assertEqual(property.owner, user)

    def test_property_str_returns_title(self):
        user = get_user_model().objects.create_user(
            username="struser",
            password="testpass123"
        )
    
        property = Property.objects.create(
            title="Beautiful Apartment",
            description="Test description",
            price=100000,
            area=80,
            bedrooms=2,
            bathrooms=1,
            floor=3,
            total_floors=6,
            city="Sofia",
            address="Test Address",
            owner=user,
            property_type=Property.PropertyType.APARTMENT,
            status=Property.Status.ACTIVE,
        )
    
        self.assertEqual(str(property), "Beautiful Apartment")

    def test_property_price_must_be_positive(self):
        user = get_user_model().objects.create_user(
            username="priceuser",
            password="testpass123"
        )

        property = Property(
            title="Test Property",
            description="Test description",
            price=0,
            area=80,
            bedrooms=2,
            bathrooms=1,
            floor=3,
            total_floors=6,
            city="Sofia",
            address="Test Address",
            owner=user,
            property_type=Property.PropertyType.APARTMENT,
            status=Property.Status.ACTIVE,
        )

        with self.assertRaises(ValidationError):
            property.full_clean()

    def test_property_area_must_be_positive(self):
        user = get_user_model().objects.create_user(
            username="areauser",
            password="testpass123"
        )

        property = Property(
            title="Test Property",
            description="Test description",
            price=100000,
            area=0,
            bedrooms=2,
            bathrooms=1,
            floor=3,
            total_floors=6,
            city="Sofia",
            address="Test Address",
            owner=user,
            property_type=Property.PropertyType.APARTMENT,
            status=Property.Status.ACTIVE,
        )

        with self.assertRaises(ValidationError):
            property.full_clean()


    def test_property_must_have_at_least_one_bedroom(self):
        user = get_user_model().objects.create_user(
            username="bedroomuser",
            password="testpass123"
        )

        property = Property(
            title="Test Property",
            description="Test description",
            price=100000,
            area=80,
            bedrooms=0,
            bathrooms=1,
            floor=3,
            total_floors=6,
            city="Sofia",
            address="Test Address",
            owner=user,
            property_type=Property.PropertyType.APARTMENT,
            status=Property.Status.ACTIVE,
        )

        with self.assertRaises(ValidationError):
            property.full_clean()


    def test_property_must_have_at_least_one_bathroom(self):
        user = get_user_model().objects.create_user(
            username="bathroomuser",
            password="testpass123"
        )

        property = Property(
            title="Test Property",
            description="Test description",
            price=100000,
            area=80,
            bedrooms=2,
            bathrooms=0,
            floor=3,
            total_floors=6,
            city="Sofia",
            address="Test Address",
            owner=user,
            property_type=Property.PropertyType.APARTMENT,
            status=Property.Status.ACTIVE,
        )

        with self.assertRaises(ValidationError):
            property.full_clean()


    def test_property_default_status_is_active(self):
        user = get_user_model().objects.create_user(
            username="statususer",
            password="testpass123"
        )

        property = Property.objects.create(
            title="Test Property",
            description="Test description",
            price=100000,
            area=80,
            bedrooms=2,
            bathrooms=1,
            floor=3,
            total_floors=6,
            city="Sofia",
            address="Test Address",
            owner=user,
            property_type=Property.PropertyType.APARTMENT,
        )

        self.assertEqual(property.status, Property.Status.ACTIVE)


    def test_property_type_is_saved_correctly(self):
        user = get_user_model().objects.create_user(
            username="typeuser",
            password="testpass123"
        )

        property = Property.objects.create(
            title="Test Property",
            description="Test description",
            price=100000,
            area=80,
            bedrooms=2,
            bathrooms=1,
            floor=3,
            total_floors=6,
            city="Sofia",
            address="Test Address",
            owner=user,
            property_type=Property.PropertyType.HOUSE,
        )

        self.assertEqual(
            property.property_type,
            Property.PropertyType.HOUSE
        )


class PropertyImageModelTest(TestCase):

    def test_property_image_is_connected_to_property(self):
        user = get_user_model().objects.create_user(
            username="imageuser",
            password="testpass123"
        )

        property = Property.objects.create(
            title="Test Property",
            description="Test description",
            price=100000,
            area=80,
            bedrooms=2,
            bathrooms=1,
            floor=3,
            total_floors=6,
            city="Sofia",
            address="Test Address",
            owner=user,
            property_type=Property.PropertyType.APARTMENT,
            status=Property.Status.ACTIVE,
        )

        property_image = PropertyImage.objects.create(
            property=property,
            image="test.jpg"
        )

        self.assertEqual(property_image.property, property)


class PropertyViewsTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="viewuser",
            password="testpass123"
        )

        self.property = Property.objects.create(
            title="Test Apartment",
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

    def test_property_list_view_returns_200(self):
        response = self.client.get(
            reverse("property_list")
        )

        self.assertEqual(response.status_code, 200)

    def test_property_list_contains_property(self):
        response = self.client.get(
            reverse("property_list")
        )

        self.assertContains(
            response,
            "Test Apartment"
        )

    def test_property_detail_view_returns_200(self):
        response = self.client.get(
            reverse(
                "property_detail",
                kwargs={"pk": self.property.pk}
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_property_detail_contains_property(self):
        response = self.client.get(
            reverse(
                "property_detail",
                kwargs={"pk": self.property.pk}
            )
        )

        self.assertContains(
            response,
            "Test Apartment"
        )

    def test_anonymous_user_cannot_create_property(self):
        response = self.client.get(
            reverse("property_create")
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)


    def test_regular_user_cannot_create_property(self):
        user = get_user_model().objects.create_user(
            username="regularuser",
            password="testpass123",
            role="USER"
        )

        self.client.login(
            username="regularuser",
            password="testpass123"
        )

        response = self.client.get(
            reverse("property_create")
        )

        self.assertEqual(response.status_code, 403)


    def test_agent_can_access_property_create(self):
        agent = get_user_model().objects.create_user(
            username="agentuser",
            password="testpass123",
            role="AGENT"
        )

        self.client.login(
            username="agentuser",
            password="testpass123"
        )

        response = self.client.get(
            reverse("property_create")
        )

        self.assertEqual(response.status_code, 200)


    def test_admin_can_access_property_create(self):
        admin = get_user_model().objects.create_user(
            username="adminuser",
            password="testpass123",
            role="ADMIN"
        )

        self.client.login(
            username="adminuser",
            password="testpass123"
        )

        response = self.client.get(
            reverse("property_create")
        )

        self.assertEqual(response.status_code, 200)

    def test_agent_can_edit_own_property(self):
        agent = get_user_model().objects.create_user(
            username="editagent",
            password="testpass123",
            role="AGENT"
        )

        self.property.owner = agent
        self.property.save()

        self.client.login(
            username="editagent",
            password="testpass123"
        )

        response = self.client.get(
            reverse(
                "property_edit",
                kwargs={"pk": self.property.pk}
            )
        )

        self.assertEqual(response.status_code, 200)


    def test_agent_cannot_edit_other_users_property(self):
        agent = get_user_model().objects.create_user(
            username="otheragent",
            password="testpass123",
            role="AGENT"
        )

        self.client.login(
            username="otheragent",
            password="testpass123"
        )

        response = self.client.get(
            reverse(
                "property_edit",
                kwargs={"pk": self.property.pk}
            )
        )

        self.assertEqual(response.status_code, 403)


    def test_admin_can_edit_any_property(self):
        admin = get_user_model().objects.create_user(
            username="editadmin",
            password="testpass123",
            role="ADMIN"
        )

        self.client.login(
            username="editadmin",
            password="testpass123"
        )

        response = self.client.get(
            reverse(
                "property_edit",
                kwargs={"pk": self.property.pk}
            )
        )

        self.assertEqual(response.status_code, 200)


    def test_agent_can_delete_own_property(self):
        agent = get_user_model().objects.create_user(
            username="deleteagent",
            password="testpass123",
            role="AGENT"
        )

        self.property.owner = agent
        self.property.save()

        self.client.login(
            username="deleteagent",
            password="testpass123"
        )

        response = self.client.post(
            reverse(
                "property_delete",
                kwargs={"pk": self.property.pk}
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Property.objects.filter(pk=self.property.pk).exists()
        )


    def test_agent_cannot_delete_other_users_property(self):
        agent = get_user_model().objects.create_user(
            username="otherdeleteagent",
            password="testpass123",
            role="AGENT"
        )

        self.client.login(
            username="otherdeleteagent",
            password="testpass123"
        )

        response = self.client.post(
            reverse(
                "property_delete",
                kwargs={"pk": self.property.pk}
            )
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            Property.objects.filter(pk=self.property.pk).exists()
        )


    def test_admin_can_delete_any_property(self):
        admin = get_user_model().objects.create_user(
            username="deleteadmin",
            password="testpass123",
            role="ADMIN"
        )

        self.client.login(
            username="deleteadmin",
            password="testpass123"
        )

        response = self.client.post(
            reverse(
                "property_delete",
                kwargs={"pk": self.property.pk}
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Property.objects.filter(pk=self.property.pk).exists()
        )

    def test_agent_can_create_property(self):
        agent = get_user_model().objects.create_user(
            username="createagent",
            password="testpass123",
            role="AGENT"
        )

        self.client.login(
            username="createagent",
            password="testpass123"
        )

        data = {
            "title": "New Apartment",
            "description": "New property description",
            "price": "200000",
            "area": "90",
            "bedrooms": "3",
            "bathrooms": "2",
            "floor": "4",
            "total_floors": "8",
            "city": "Sofia",
            "address": "New Address",
            "property_type": Property.PropertyType.APARTMENT,
            "status": Property.Status.ACTIVE,
        }

        response = self.client.post(
            reverse("property_create"),
            data
        )

        self.assertEqual(response.status_code, 302)

        created_property = Property.objects.get(
            title="New Apartment"
        )

        self.assertEqual(
            created_property.owner,
            agent
        )


    def test_regular_user_cannot_create_property_with_post(self):
        user = get_user_model().objects.create_user(
            username="postuser",
            password="testpass123",
            role="USER"
        )

        self.client.login(
            username="postuser",
            password="testpass123"
        )

        response = self.client.post(
            reverse("property_create"),
            {
                "title": "Unauthorized Property",
            }
        )

        self.assertEqual(response.status_code, 403)

        self.assertFalse(
            Property.objects.filter(
                title="Unauthorized Property"
            ).exists()
        )