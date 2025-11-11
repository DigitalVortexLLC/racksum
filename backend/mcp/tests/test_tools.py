"""
Tests for MCP server tool definitions
"""
from django.test import TestCase
from mcp.tools import get_tool_definitions
from mcp.types import Tool


class TestToolDefinitions(TestCase):
    """Test cases for MCP tool definitions"""

    def test_get_tool_definitions_returns_list(self):
        """Test that get_tool_definitions returns a list"""
        tools = get_tool_definitions()
        self.assertIsInstance(tools, list)

    def test_get_tool_definitions_not_empty(self):
        """Test that tool definitions list is not empty"""
        tools = get_tool_definitions()
        self.assertTrue(len(tools) > 0)

    def test_all_tools_are_tool_objects(self):
        """Test that all returned items are Tool objects"""
        tools = get_tool_definitions()
        for tool in tools:
            self.assertIsInstance(tool, Tool)

    def test_tool_count(self):
        """Test that we have exactly 5 tools defined"""
        tools = get_tool_definitions()
        self.assertEqual(len(tools), 5)

    def test_get_site_stats_tool(self):
        """Test get_site_stats tool definition"""
        tools = get_tool_definitions()
        site_stats_tool = next((t for t in tools if t.name == "get_site_stats"), None)

        self.assertIsNotNone(site_stats_tool)
        self.assertEqual(site_stats_tool.name, "get_site_stats")
        self.assertIn("statistics", site_stats_tool.description.lower())
        self.assertIsInstance(site_stats_tool.inputSchema, dict)
        self.assertEqual(site_stats_tool.inputSchema["type"], "object")
        self.assertEqual(site_stats_tool.inputSchema["required"], [])

    def test_get_site_details_tool(self):
        """Test get_site_details tool definition"""
        tools = get_tool_definitions()
        site_details_tool = next((t for t in tools if t.name == "get_site_details"), None)

        self.assertIsNotNone(site_details_tool)
        self.assertEqual(site_details_tool.name, "get_site_details")
        self.assertIn("site", site_details_tool.description.lower())
        self.assertIn("site_name", site_details_tool.inputSchema["properties"])
        self.assertEqual(site_details_tool.inputSchema["required"], ["site_name"])

    def test_get_rack_details_tool(self):
        """Test get_rack_details tool definition"""
        tools = get_tool_definitions()
        rack_details_tool = next((t for t in tools if t.name == "get_rack_details"), None)

        self.assertIsNotNone(rack_details_tool)
        self.assertEqual(rack_details_tool.name, "get_rack_details")
        self.assertIn("rack", rack_details_tool.description.lower())
        self.assertIn("site_name", rack_details_tool.inputSchema["properties"])
        self.assertIn("rack_name", rack_details_tool.inputSchema["properties"])
        self.assertIn("site_name", rack_details_tool.inputSchema["required"])
        self.assertIn("rack_name", rack_details_tool.inputSchema["required"])

    def test_get_available_resources_tool(self):
        """Test get_available_resources tool definition"""
        tools = get_tool_definitions()
        resources_tool = next((t for t in tools if t.name == "get_available_resources"), None)

        self.assertIsNotNone(resources_tool)
        self.assertEqual(resources_tool.name, "get_available_resources")
        self.assertIn("device", resources_tool.description.lower())
        self.assertIn("category", resources_tool.inputSchema["properties"])
        self.assertIn("limit", resources_tool.inputSchema["properties"])
        # category and limit are optional
        self.assertEqual(resources_tool.inputSchema.get("required", []), [])

    def test_get_resource_summary_tool(self):
        """Test get_resource_summary tool definition"""
        tools = get_tool_definitions()
        summary_tool = next((t for t in tools if t.name == "get_resource_summary"), None)

        self.assertIsNotNone(summary_tool)
        self.assertEqual(summary_tool.name, "get_resource_summary")
        self.assertIn("resource", summary_tool.description.lower())
        self.assertEqual(summary_tool.inputSchema["required"], [])

    def test_all_tool_names_unique(self):
        """Test that all tool names are unique"""
        tools = get_tool_definitions()
        tool_names = [t.name for t in tools]
        self.assertEqual(len(tool_names), len(set(tool_names)))

    def test_all_tools_have_descriptions(self):
        """Test that all tools have non-empty descriptions"""
        tools = get_tool_definitions()
        for tool in tools:
            self.assertTrue(tool.description)
            self.assertGreater(len(tool.description), 10)

    def test_all_tools_have_valid_schemas(self):
        """Test that all tools have valid input schemas"""
        tools = get_tool_definitions()
        for tool in tools:
            schema = tool.inputSchema
            self.assertIsInstance(schema, dict)
            self.assertEqual(schema.get("type"), "object")
            self.assertIn("properties", schema)
            self.assertIn("required", schema)

    def test_tool_schema_property_types(self):
        """Test that tool schema properties have correct types"""
        tools = get_tool_definitions()

        # Check get_site_details
        site_details = next(t for t in tools if t.name == "get_site_details")
        self.assertEqual(
            site_details.inputSchema["properties"]["site_name"]["type"],
            "string"
        )

        # Check get_rack_details
        rack_details = next(t for t in tools if t.name == "get_rack_details")
        self.assertEqual(
            rack_details.inputSchema["properties"]["site_name"]["type"],
            "string"
        )
        self.assertEqual(
            rack_details.inputSchema["properties"]["rack_name"]["type"],
            "string"
        )

        # Check get_available_resources
        resources = next(t for t in tools if t.name == "get_available_resources")
        self.assertEqual(
            resources.inputSchema["properties"]["category"]["type"],
            "string"
        )
        self.assertEqual(
            resources.inputSchema["properties"]["limit"]["type"],
            "integer"
        )
