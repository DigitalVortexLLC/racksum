from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .models import Site, Device, Rack


class SiteModelTest(TestCase):
    """Test cases for Site model"""

    def setUp(self):
        self.site = Site.objects.create(name="Test Site", description="A test site for unit tests")

    def test_site_creation(self):
        """Test that a site can be created successfully"""
        self.assertEqual(self.site.name, "Test Site")
        self.assertEqual(self.site.description, "A test site for unit tests")
        self.assertIsNotNone(self.site.uuid)
        self.assertIsNotNone(self.site.created_at)

    def test_site_str_representation(self):
        """Test string representation of site"""
        self.assertEqual(str(self.site), "Test Site")


class DeviceModelTest(TestCase):
    """Test cases for Device model"""

    def setUp(self):
        self.device = Device.objects.create(
            device_id="test-device-001",
            name="Test Device",
            category="servers",
            ru_size=2,
            power_draw=500,
            power_ports_used=2,
            color="#FF0000",
            description="Test server device",
        )

    def test_device_creation(self):
        """Test that a device can be created successfully"""
        self.assertEqual(self.device.device_id, "test-device-001")
        self.assertEqual(self.device.name, "Test Device")
        self.assertEqual(self.device.ru_size, 2)
        self.assertEqual(self.device.power_draw, 500)

    def test_device_str_representation(self):
        """Test string representation of device"""
        self.assertEqual(str(self.device), "Test Device (test-device-001)")


class APIEndpointTest(TestCase):
    """Test cases for API endpoints"""

    def setUp(self):
        self.client = Client()
        self.site = Site.objects.create(name="API Test Site", description="Site for API testing")

    def test_auth_config_endpoint(self):
        """Test auth config endpoint returns correct data"""
        response = self.client.get(reverse("auth-config"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("require_auth", response.json())
        self.assertIn("passkey_supported", response.json())

    def test_devices_list_endpoint(self):
        """Test devices list endpoint"""
        Device.objects.create(
            device_id="api-test-device", name="API Test Device", category="network", ru_size=1, power_draw=100
        )
        response = self.client.get("/api/devices")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_sites_list_endpoint(self):
        """Test sites list endpoint"""
        response = self.client.get("/api/sites")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_site_detail_endpoint(self):
        """Test site detail endpoint"""
        response = self.client.get(f"/api/sites/{self.site.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["name"], "API Test Site")

    def test_site_by_uuid_endpoint(self):
        """Test fetching site by UUID"""
        response = self.client.get(f"/api/sites/by-uuid/{self.site.uuid}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["uuid"], str(self.site.uuid))


class RackModelTest(TestCase):
    """Test cases for Rack model"""

    def setUp(self):
        self.site = Site.objects.create(name="Rack Test Site")
        self.rack = Rack.objects.create(
            site=self.site, name="Test Rack", ru_height=42, description="Test rack for unit tests"
        )

    def test_rack_creation(self):
        """Test that a rack can be created successfully"""
        self.assertEqual(self.rack.name, "Test Rack")
        self.assertEqual(self.rack.ru_height, 42)
        self.assertEqual(self.rack.site, self.site)

    def test_power_utilization_empty_rack(self):
        """Test power utilization for empty rack is 0"""
        self.assertEqual(self.rack.get_power_utilization(), 0)

    def test_hvac_load_empty_rack(self):
        """Test HVAC load for empty rack is 0"""
        self.assertEqual(self.rack.get_hvac_load(), 0)

    def test_power_ports_empty_rack(self):
        """Test power ports count for empty rack is 0"""
        self.assertEqual(self.rack.get_power_ports_used(), 0)
