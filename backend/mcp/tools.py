"""
MCP tool definitions for RackSum datacenter management
"""
from mcp.types import Tool


def get_tool_definitions() -> list[Tool]:
    """Return list of available MCP tools"""
    return [
        Tool(
            name="get_site_stats",
            description="Get statistics for all sites including rack count, device count, and resource usage",
            inputSchema={
                "type": "object",
                "properties": {
                    "output_format": {
                        "type": "string",
                        "enum": ["text", "json"],
                        "description": "Output format: 'text' (default, human-readable) or 'json' (structured data)",
                        "default": "text"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_site_details",
            description="Get detailed information about a specific site including all racks and resource usage",
            inputSchema={
                "type": "object",
                "properties": {
                    "site_name": {
                        "type": "string",
                        "description": "Name of the site to get details for"
                    },
                    "output_format": {
                        "type": "string",
                        "enum": ["text", "json"],
                        "description": "Output format: 'text' (default, human-readable) or 'json' (structured data)",
                        "default": "text"
                    }
                },
                "required": ["site_name"]
            }
        ),
        Tool(
            name="get_rack_details",
            description="Get detailed information about a specific rack including devices and resource usage",
            inputSchema={
                "type": "object",
                "properties": {
                    "site_name": {
                        "type": "string",
                        "description": "Name of the site containing the rack"
                    },
                    "rack_name": {
                        "type": "string",
                        "description": "Name of the rack to get details for"
                    },
                    "output_format": {
                        "type": "string",
                        "enum": ["text", "json"],
                        "description": "Output format: 'text' (default, human-readable) or 'json' (structured data)",
                        "default": "text"
                    }
                },
                "required": ["site_name", "rack_name"]
            }
        ),
        Tool(
            name="get_available_resources",
            description="Get information about available device types and their specifications",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Filter devices by category (optional)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of devices to return (optional, default: no limit)"
                    },
                    "output_format": {
                        "type": "string",
                        "enum": ["text", "json"],
                        "description": "Output format: 'text' (default, human-readable) or 'json' (structured data)",
                        "default": "text"
                    }
                }
            }
        ),
        Tool(
            name="get_resource_summary",
            description="Get overall resource utilization summary across all sites",
            inputSchema={
                "type": "object",
                "properties": {
                    "output_format": {
                        "type": "string",
                        "enum": ["text", "json"],
                        "description": "Output format: 'text' (default, human-readable) or 'json' (structured data)",
                        "default": "text"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="create_device",
            description="Create a new device type that can be placed in racks",
            inputSchema={
                "type": "object",
                "properties": {
                    "device_id": {"type": "string", "description": "Unique identifier for the device"},
                    "name": {"type": "string", "description": "Display name of the device"},
                    "category": {"type": "string", "description": "Device category (e.g., Server, Network, Storage)"},
                    "ru_size": {"type": "integer", "description": "Rack unit size of the device"},
                    "power_draw": {"type": "integer", "description": "Power consumption in watts"},
                    "power_ports_used": {
                        "type": "integer",
                        "description": "Number of PDU power ports required (default: 1)",
                    },
                    "color": {"type": "string", "description": "Hex color code for display (default: #000000)"},
                    "description": {"type": "string", "description": "Optional description of the device"},
                },
                "required": ["device_id", "name", "category", "ru_size", "power_draw"],
            },
        ),
        Tool(
            name="create_rack",
            description="Create a new rack in a site",
            inputSchema={
                "type": "object",
                "properties": {
                    "site_name": {"type": "string", "description": "Name of the site to add the rack to"},
                    "rack_name": {"type": "string", "description": "Name of the new rack"},
                    "ru_height": {"type": "integer", "description": "Height of the rack in rack units (default: 42)"},
                    "description": {"type": "string", "description": "Optional description of the rack"},
                },
                "required": ["site_name", "rack_name"],
            },
        ),
        Tool(
            name="delete_rack",
            description="Delete a rack from a site",
            inputSchema={
                "type": "object",
                "properties": {
                    "site_name": {"type": "string", "description": "Name of the site containing the rack"},
                    "rack_name": {"type": "string", "description": "Name of the rack to delete"},
                },
                "required": ["site_name", "rack_name"],
            },
        ),
        Tool(
            name="update_site_name",
            description="Change the name of an existing site",
            inputSchema={
                "type": "object",
                "properties": {
                    "old_name": {"type": "string", "description": "Current name of the site"},
                    "new_name": {"type": "string", "description": "New name for the site"},
                },
                "required": ["old_name", "new_name"],
            },
        ),
        Tool(
            name="create_device_group",
            description="Create a new device group for organizing device types",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name of the device group"},
                    "description": {"type": "string", "description": "Optional description of the device group"},
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="create_provider",
            description="Create a new hardware/equipment provider",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name of the provider"},
                    "description": {"type": "string", "description": "Optional description of the provider"},
                    "website": {"type": "string", "description": "Optional website URL of the provider"},
                },
                "required": ["name"],
            },
        ),
    ]
