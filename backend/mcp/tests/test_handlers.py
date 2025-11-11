"""
Tests for MCP server handlers
"""
import pytest
from django.test import TestCase
from mcp.types import TextContent
from api.models import Site, Rack, Device, RackDevice
from mcp import handlers


@pytest.mark.django_db
class TestGetSiteStats(TestCase):
    """Test cases for get_site_stats handler"""

    @pytest.mark.asyncio
    async def test_get_site_stats_empty_database(self):
        """Test get_site_stats with no sites in database"""
        result = await handlers.get_site_stats()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], TextContent)
        self.assertIn("No sites found", result[0].text)

    @pytest.mark.asyncio
    async def test_get_site_stats_with_sites(self):
        """Test get_site_stats with sites in database"""
        # Create test data
        site = Site.objects.create(name="Test Site", description="Test Description")
        rack = Rack.objects.create(site=site, name="Rack-A1", ru_height=42)

        result = await handlers.get_site_stats()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], TextContent)
        self.assertIn("Test Site", result[0].text)
        self.assertIn("SITE STATISTICS", result[0].text)
        self.assertIn("Racks: 1", result[0].text)

    @pytest.mark.asyncio
    async def test_get_site_stats_with_devices(self):
        """Test get_site_stats with devices installed"""
        # Create test data
        site = Site.objects.create(name="Datacenter 1")
        rack = Rack.objects.create(site=site, name="Rack-A1", ru_height=42)
        device = Device.objects.create(
            device_id="test-server",
            name="Test Server",
            category="Server",
            ru_size=2,
            power_draw=500,
            color="#FF0000"
        )
        RackDevice.objects.create(
            rack=rack,
            device=device,
            position=1,
            instance_name="Server-001"
        )

        result = await handlers.get_site_stats()

        self.assertIn("Devices: 1", result[0].text)
        self.assertIn("Total Power:", result[0].text)
        self.assertIn("Total HVAC Load:", result[0].text)

    @pytest.mark.asyncio
    async def test_get_site_stats_multiple_sites(self):
        """Test get_site_stats with multiple sites"""
        Site.objects.create(name="Site 1")
        Site.objects.create(name="Site 2")
        Site.objects.create(name="Site 3")

        result = await handlers.get_site_stats()

        text = result[0].text
        self.assertIn("Site 1", text)
        self.assertIn("Site 2", text)
        self.assertIn("Site 3", text)


@pytest.mark.django_db
class TestGetSiteDetails(TestCase):
    """Test cases for get_site_details handler"""

    @pytest.mark.asyncio
    async def test_get_site_details_not_found(self):
        """Test get_site_details with non-existent site"""
        result = await handlers.get_site_details("NonexistentSite")

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIn("not found", result[0].text)

    @pytest.mark.asyncio
    async def test_get_site_details_existing_site(self):
        """Test get_site_details with existing site"""
        site = Site.objects.create(name="Test Site", description="Test Description")

        result = await handlers.get_site_details("Test Site")

        text = result[0].text
        self.assertIn("SITE DETAILS: Test Site", text)
        self.assertIn("Test Description", text)
        self.assertIn("Total Racks: 0", text)

    @pytest.mark.asyncio
    async def test_get_site_details_case_insensitive(self):
        """Test get_site_details with case-insensitive lookup"""
        Site.objects.create(name="Test Site")

        result = await handlers.get_site_details("test site")

        text = result[0].text
        self.assertIn("SITE DETAILS: Test Site", text)

    @pytest.mark.asyncio
    async def test_get_site_details_with_racks(self):
        """Test get_site_details with racks"""
        site = Site.objects.create(name="Datacenter 1")
        Rack.objects.create(site=site, name="Rack-A1", ru_height=42, description="Front row")
        Rack.objects.create(site=site, name="Rack-A2", ru_height=42)

        result = await handlers.get_site_details("Datacenter 1")

        text = result[0].text
        self.assertIn("Total Racks: 2", text)
        self.assertIn("Rack-A1", text)
        self.assertIn("Rack-A2", text)
        self.assertIn("Front row", text)


@pytest.mark.django_db
class TestGetRackDetails(TestCase):
    """Test cases for get_rack_details handler"""

    @pytest.mark.asyncio
    async def test_get_rack_details_site_not_found(self):
        """Test get_rack_details with non-existent site"""
        result = await handlers.get_rack_details("NonexistentSite", "Rack-A1")

        self.assertIn("Site 'NonexistentSite' not found", result[0].text)

    @pytest.mark.asyncio
    async def test_get_rack_details_rack_not_found(self):
        """Test get_rack_details with non-existent rack"""
        Site.objects.create(name="Test Site")

        result = await handlers.get_rack_details("Test Site", "NonexistentRack")

        self.assertIn("Rack 'NonexistentRack' not found", result[0].text)

    @pytest.mark.asyncio
    async def test_get_rack_details_existing_rack(self):
        """Test get_rack_details with existing rack"""
        site = Site.objects.create(name="Datacenter 1")
        rack = Rack.objects.create(
            site=site,
            name="Rack-A1",
            ru_height=42,
            description="Main rack"
        )

        result = await handlers.get_rack_details("Datacenter 1", "Rack-A1")

        text = result[0].text
        self.assertIn("RACK DETAILS: Datacenter 1 - Rack-A1", text)
        self.assertIn("Main rack", text)
        self.assertIn("Height: 42U", text)
        self.assertIn("Space Used:", text)
        self.assertIn("No devices installed", text)

    @pytest.mark.asyncio
    async def test_get_rack_details_case_insensitive(self):
        """Test get_rack_details with case-insensitive lookup"""
        site = Site.objects.create(name="Datacenter 1")
        Rack.objects.create(site=site, name="Rack-A1", ru_height=42)

        result = await handlers.get_rack_details("datacenter 1", "rack-a1")

        text = result[0].text
        self.assertIn("RACK DETAILS:", text)

    @pytest.mark.asyncio
    async def test_get_rack_details_with_devices(self):
        """Test get_rack_details with installed devices"""
        site = Site.objects.create(name="Datacenter 1")
        rack = Rack.objects.create(site=site, name="Rack-A1", ru_height=42)
        device = Device.objects.create(
            device_id="test-server",
            name="Dell R740",
            category="Server",
            ru_size=2,
            power_draw=750,
            color="#0000FF"
        )
        RackDevice.objects.create(
            rack=rack,
            device=device,
            position=1,
            instance_name="DB-Server-01"
        )

        result = await handlers.get_rack_details("Datacenter 1", "Rack-A1")

        text = result[0].text
        self.assertIn("--- DEVICES ---", text)
        self.assertIn("DB-Server-01", text)
        self.assertIn("Dell R740", text)
        self.assertIn("Server", text)
        self.assertIn("Position: RU 1", text)
        self.assertIn("Power: 750 W", text)


@pytest.mark.django_db
class TestGetAvailableResources(TestCase):
    """Test cases for get_available_resources handler"""

    @pytest.mark.asyncio
    async def test_get_available_resources_empty(self):
        """Test get_available_resources with no devices"""
        result = await handlers.get_available_resources()

        self.assertIn("No devices found", result[0].text)

    @pytest.mark.asyncio
    async def test_get_available_resources_with_devices(self):
        """Test get_available_resources with devices"""
        Device.objects.create(
            device_id="server-1",
            name="Dell R740",
            category="Server",
            ru_size=2,
            power_draw=750,
            color="#FF0000"
        )
        Device.objects.create(
            device_id="switch-1",
            name="Cisco Nexus",
            category="Network",
            ru_size=1,
            power_draw=200,
            color="#00FF00"
        )

        result = await handlers.get_available_resources()

        text = result[0].text
        self.assertIn("AVAILABLE DEVICE TYPES", text)
        self.assertIn("Dell R740", text)
        self.assertIn("Cisco Nexus", text)
        self.assertIn("Server", text)
        self.assertIn("Network", text)

    @pytest.mark.asyncio
    async def test_get_available_resources_with_category_filter(self):
        """Test get_available_resources with category filter"""
        Device.objects.create(
            device_id="server-1",
            name="Dell R740",
            category="Server",
            ru_size=2,
            power_draw=750,
            color="#FF0000"
        )
        Device.objects.create(
            device_id="switch-1",
            name="Cisco Nexus",
            category="Network",
            ru_size=1,
            power_draw=200,
            color="#00FF00"
        )

        result = await handlers.get_available_resources(category="Server")

        text = result[0].text
        self.assertIn("Dell R740", text)
        self.assertNotIn("Cisco Nexus", text)

    @pytest.mark.asyncio
    async def test_get_available_resources_with_limit(self):
        """Test get_available_resources with limit"""
        for i in range(5):
            Device.objects.create(
                device_id=f"device-{i}",
                name=f"Device {i}",
                category="Server",
                ru_size=1,
                power_draw=100,
                color="#FF0000"
            )

        result = await handlers.get_available_resources(limit=2)

        text = result[0].text
        self.assertIn("Total device types shown: 2", text)
        self.assertIn("Showing first 2 of 5 total devices", text)

    @pytest.mark.asyncio
    async def test_get_available_resources_no_matching_category(self):
        """Test get_available_resources with non-matching category"""
        Device.objects.create(
            device_id="server-1",
            name="Dell R740",
            category="Server",
            ru_size=2,
            power_draw=750,
            color="#FF0000"
        )

        result = await handlers.get_available_resources(category="NonexistentCategory")

        self.assertIn("No devices found in category", result[0].text)


@pytest.mark.django_db
class TestGetResourceSummary(TestCase):
    """Test cases for get_resource_summary handler"""

    @pytest.mark.asyncio
    async def test_get_resource_summary_empty(self):
        """Test get_resource_summary with no data"""
        result = await handlers.get_resource_summary()

        self.assertIn("No sites found", result[0].text)

    @pytest.mark.asyncio
    async def test_get_resource_summary_with_data(self):
        """Test get_resource_summary with complete data"""
        site1 = Site.objects.create(name="Site 1")
        site2 = Site.objects.create(name="Site 2")

        rack1 = Rack.objects.create(site=site1, name="Rack-A1", ru_height=42)
        rack2 = Rack.objects.create(site=site2, name="Rack-B1", ru_height=42)

        device = Device.objects.create(
            device_id="server-1",
            name="Server",
            category="Server",
            ru_size=2,
            power_draw=500,
            color="#FF0000"
        )

        RackDevice.objects.create(rack=rack1, device=device, position=1)
        RackDevice.objects.create(rack=rack2, device=device, position=1)

        result = await handlers.get_resource_summary()

        text = result[0].text
        self.assertIn("RESOURCE UTILIZATION SUMMARY", text)
        self.assertIn("Total Sites: 2", text)
        self.assertIn("Total Racks: 2", text)
        self.assertIn("Total Devices Installed: 2", text)
        self.assertIn("Device Types Available: 1", text)
        self.assertIn("Total RU Capacity: 84U", text)
        self.assertIn("Total RU Used: 4U", text)
        self.assertIn("Utilization:", text)
        self.assertIn("Total Power Draw:", text)
        self.assertIn("Total HVAC Load:", text)
        self.assertIn("Average per Rack:", text)

    @pytest.mark.asyncio
    async def test_get_resource_summary_utilization_calculation(self):
        """Test that utilization percentage is calculated correctly"""
        site = Site.objects.create(name="Test Site")
        rack = Rack.objects.create(site=site, name="Rack-A1", ru_height=42)

        device = Device.objects.create(
            device_id="server-1",
            name="Server",
            category="Server",
            ru_size=21,  # Exactly half
            power_draw=500,
            color="#FF0000"
        )

        RackDevice.objects.create(rack=rack, device=device, position=1)

        result = await handlers.get_resource_summary()

        text = result[0].text
        self.assertIn("Total RU Capacity: 42U", text)
        self.assertIn("Total RU Used: 21U", text)
        self.assertIn("Utilization: 50.0%", text)
