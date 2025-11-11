"""
MCP Server for RackSum - Provides site stats and resource information
"""

import os
import sys
import django
import asyncio
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server
from asgiref.sync import sync_to_async
import argparse
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import Response
import uvicorn
import json

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from api.models import Site, Rack, Device, RackDevice, DeviceGroup, Provider


# Create MCP server instance
app = Server("racksum-stats")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools"""
    return [
        Tool(
            name="get_site_stats",
            description="Get statistics for all sites including rack count, device count, and resource usage",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="get_site_details",
            description="Get detailed information about a specific site including all racks and resource usage",
            inputSchema={
                "type": "object",
                "properties": {"site_name": {"type": "string", "description": "Name of the site to get details for"}},
                "required": ["site_name"],
            },
        ),
        Tool(
            name="get_rack_details",
            description="Get detailed information about a specific rack including devices and resource usage",
            inputSchema={
                "type": "object",
                "properties": {
                    "site_name": {"type": "string", "description": "Name of the site containing the rack"},
                    "rack_name": {"type": "string", "description": "Name of the rack to get details for"},
                },
                "required": ["site_name", "rack_name"],
            },
        ),
        Tool(
            name="get_available_resources",
            description="Get information about available device types and their specifications",
            inputSchema={
                "type": "object",
                "properties": {"category": {"type": "string", "description": "Filter devices by category (optional)"}},
            },
        ),
        Tool(
            name="get_resource_summary",
            description="Get overall resource utilization summary across all sites",
            inputSchema={"type": "object", "properties": {}, "required": []},
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


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""

    if name == "get_site_stats":
        return await get_site_stats()
    elif name == "get_site_details":
        site_name = arguments.get("site_name")
        if not site_name:
            return [TextContent(type="text", text="Error: site_name is required")]
        return await get_site_details(site_name)
    elif name == "get_rack_details":
        site_name = arguments.get("site_name")
        rack_name = arguments.get("rack_name")
        if not site_name or not rack_name:
            return [TextContent(type="text", text="Error: site_name and rack_name are required")]
        return await get_rack_details(site_name, rack_name)
    elif name == "get_available_resources":
        category = arguments.get("category")
        return await get_available_resources(category)
    elif name == "get_resource_summary":
        return await get_resource_summary()
    elif name == "create_device":
        return await create_device(arguments)
    elif name == "create_rack":
        return await create_rack(arguments)
    elif name == "delete_rack":
        site_name = arguments.get("site_name")
        rack_name = arguments.get("rack_name")
        if not site_name or not rack_name:
            return [TextContent(type="text", text="Error: site_name and rack_name are required")]
        return await delete_rack(site_name, rack_name)
    elif name == "update_site_name":
        old_name = arguments.get("old_name")
        new_name = arguments.get("new_name")
        if not old_name or not new_name:
            return [TextContent(type="text", text="Error: old_name and new_name are required")]
        return await update_site_name(old_name, new_name)
    elif name == "create_device_group":
        return await create_device_group(arguments)
    elif name == "create_provider":
        return await create_provider(arguments)
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def get_site_stats() -> list[TextContent]:
    """Get statistics for all sites"""

    @sync_to_async
    def get_stats():
        sites = list(Site.objects.all())

        if not sites:
            return "No sites found in the database."

        stats = []
        stats.append("=== SITE STATISTICS ===\n")

        for site in sites:
            racks = list(site.racks.all())
            total_racks = len(racks)
            total_devices = sum(rack.rack_devices.count() for rack in racks)
            total_power = sum(rack.get_power_utilization() for rack in racks)
            total_hvac = sum(rack.get_hvac_load() for rack in racks)

            stats.append(f"\n📍 Site: {site.name}")
            if site.description:
                stats.append(f"   Description: {site.description}")
            stats.append(f"   Racks: {total_racks}")
            stats.append(f"   Devices: {total_devices}")
            stats.append(f"   Total Power: {total_power:,.0f} W ({total_power/1000:.2f} kW)")
            stats.append(f"   Total HVAC Load: {total_hvac:,.0f} BTU/hr ({total_hvac/12000:.2f} tons)")
            stats.append(f"   Created: {site.created_at.strftime('%Y-%m-%d %H:%M')}")

        return "\n".join(stats)

    result = await get_stats()
    return [TextContent(type="text", text=result)]


async def get_site_details(site_name: str) -> list[TextContent]:
    """Get detailed information about a specific site"""

    @sync_to_async
    def get_details():
        try:
            site = Site.objects.get(name=site_name)
        except Site.DoesNotExist:
            return f"Site '{site_name}' not found."

        details = []
        details.append(f"=== SITE DETAILS: {site.name} ===\n")

        if site.description:
            details.append(f"Description: {site.description}")
        details.append(f"Created: {site.created_at.strftime('%Y-%m-%d %H:%M')}")
        details.append(f"Last Updated: {site.updated_at.strftime('%Y-%m-%d %H:%M')}\n")

        racks = list(site.racks.all())
        details.append(f"Total Racks: {len(racks)}\n")

        if racks:
            details.append("--- RACKS ---")
            for rack in racks:
                devices = list(rack.rack_devices.all())
                power = rack.get_power_utilization()
                hvac = rack.get_hvac_load()
                ru_used = sum(device.device.ru_size for device in devices)
                ru_available = rack.ru_height - ru_used

                details.append(f"\n🔲 Rack: {rack.name}")
                if rack.description:
                    details.append(f"   Description: {rack.description}")
                details.append(f"   Height: {rack.ru_height}U")
                details.append(f"   Space Used: {ru_used}U / {rack.ru_height}U ({(ru_used/rack.ru_height*100):.1f}%)")
                details.append(f"   Available: {ru_available}U")
                details.append(f"   Devices: {len(devices)}")
                details.append(f"   Power: {power:,.0f} W ({power/1000:.2f} kW)")
                details.append(f"   HVAC Load: {hvac:,.0f} BTU/hr")

        return "\n".join(details)

    result = await get_details()
    return [TextContent(type="text", text=result)]


async def get_rack_details(site_name: str, rack_name: str) -> list[TextContent]:
    """Get detailed information about a specific rack"""

    @sync_to_async
    def get_details():
        try:
            site = Site.objects.get(name=site_name)
            rack = Rack.objects.get(site=site, name=rack_name)
        except Site.DoesNotExist:
            return f"Site '{site_name}' not found."
        except Rack.DoesNotExist:
            return f"Rack '{rack_name}' not found in site '{site_name}'."

        details = []
        details.append(f"=== RACK DETAILS: {site.name} - {rack.name} ===\n")

        if rack.description:
            details.append(f"Description: {rack.description}")
        details.append(f"Height: {rack.ru_height}U")
        details.append(f"Created: {rack.created_at.strftime('%Y-%m-%d %H:%M')}")
        details.append(f"Last Updated: {rack.updated_at.strftime('%Y-%m-%d %H:%M')}\n")

        devices = list(rack.rack_devices.all().select_related("device"))
        ru_used = sum(device.device.ru_size for device in devices)
        ru_available = rack.ru_height - ru_used
        power = rack.get_power_utilization()
        hvac = rack.get_hvac_load()

        details.append(f"Space Used: {ru_used}U / {rack.ru_height}U ({(ru_used/rack.ru_height*100):.1f}%)")
        details.append(f"Space Available: {ru_available}U")
        details.append(f"Total Power: {power:,.0f} W ({power/1000:.2f} kW)")
        details.append(f"HVAC Load: {hvac:,.0f} BTU/hr ({hvac/12000:.2f} tons)\n")

        if devices:
            details.append("--- DEVICES ---")
            for rack_device in devices:
                device = rack_device.device
                display_name = rack_device.instance_name or device.name

                details.append(f"\n⚙️  {display_name}")
                details.append(f"   Type: {device.name}")
                details.append(f"   Category: {device.category}")
                details.append(f"   Position: RU {rack_device.position}")
                details.append(f"   Size: {device.ru_size}U")
                details.append(f"   Power: {device.power_draw} W")
                details.append(f"   Heat: {device.power_draw * 3.41:.0f} BTU/hr")
        else:
            details.append("No devices installed in this rack.")

        return "\n".join(details)

    result = await get_details()
    return [TextContent(type="text", text=result)]


async def get_available_resources(category: str = None) -> list[TextContent]:
    """Get information about available device types"""

    @sync_to_async
    def get_resources():
        devices = Device.objects.all()

        if category:
            devices = devices.filter(category__icontains=category)

        devices_list = list(devices)

        if not devices_list:
            msg = f"No devices found" + (f" in category '{category}'" if category else "")
            return msg + "."

        details = []
        details.append("=== AVAILABLE DEVICE TYPES ===\n")

        # Group by category
        categories = {}
        for device in devices_list:
            if device.category not in categories:
                categories[device.category] = []
            categories[device.category].append(device)

        for cat, cat_devices in sorted(categories.items()):
            details.append(f"\n📦 {cat}")
            for device in cat_devices:
                details.append(f"\n   • {device.name} ({device.device_id})")
                if device.description:
                    details.append(f"     Description: {device.description}")
                details.append(f"     Size: {device.ru_size}U")
                details.append(f"     Power: {device.power_draw} W")
                details.append(f"     Heat: {device.power_draw * 3.41:.0f} BTU/hr")
                details.append(f"     Color: {device.color}")

        details.append(f"\n\nTotal device types: {len(devices_list)}")

        return "\n".join(details)

    result = await get_resources()
    return [TextContent(type="text", text=result)]


async def get_resource_summary() -> list[TextContent]:
    """Get overall resource utilization summary"""

    @sync_to_async
    def get_summary():
        sites = list(Site.objects.all())

        if not sites:
            return "No sites found in the database."

        summary = []
        summary.append("=== RESOURCE UTILIZATION SUMMARY ===\n")

        total_sites = len(sites)
        total_racks = Rack.objects.count()
        total_rack_devices = RackDevice.objects.count()
        total_device_types = Device.objects.count()

        # Calculate overall power and HVAC
        overall_power = 0
        overall_hvac = 0
        total_ru_capacity = 0
        total_ru_used = 0

        for rack in Rack.objects.all():
            overall_power += rack.get_power_utilization()
            overall_hvac += rack.get_hvac_load()
            total_ru_capacity += rack.ru_height
            total_ru_used += sum(device.device.ru_size for device in rack.rack_devices.all())

        summary.append(f"Total Sites: {total_sites}")
        summary.append(f"Total Racks: {total_racks}")
        summary.append(f"Total Devices Installed: {total_rack_devices}")
        summary.append(f"Device Types Available: {total_device_types}\n")

        summary.append("--- CAPACITY ---")
        summary.append(f"Total RU Capacity: {total_ru_capacity}U")
        summary.append(f"Total RU Used: {total_ru_used}U")
        summary.append(f"Total RU Available: {total_ru_capacity - total_ru_used}U")
        if total_ru_capacity > 0:
            summary.append(f"Utilization: {(total_ru_used/total_ru_capacity*100):.1f}%\n")

        summary.append("--- POWER & COOLING ---")
        summary.append(f"Total Power Draw: {overall_power:,.0f} W ({overall_power/1000:.2f} kW)")
        summary.append(f"Total HVAC Load: {overall_hvac:,.0f} BTU/hr ({overall_hvac/12000:.2f} tons)")

        if total_racks > 0:
            avg_power_per_rack = overall_power / total_racks
            summary.append(f"\nAverage per Rack: {avg_power_per_rack:,.0f} W ({avg_power_per_rack/1000:.2f} kW)")

        return "\n".join(summary)

    result = await get_summary()
    return [TextContent(type="text", text=result)]


async def create_device(arguments: dict) -> list[TextContent]:
    """Create a new device type"""

    @sync_to_async
    def create():
        try:
            device = Device.objects.create(
                device_id=arguments.get("device_id"),
                name=arguments.get("name"),
                category=arguments.get("category"),
                ru_size=arguments.get("ru_size"),
                power_draw=arguments.get("power_draw"),
                power_ports_used=arguments.get("power_ports_used", 1),
                color=arguments.get("color", "#000000"),
                description=arguments.get("description", ""),
            )
            return f"✅ Device created successfully!\n\nDevice ID: {device.device_id}\nName: {device.name}\nCategory: {device.category}\nSize: {device.ru_size}U\nPower: {device.power_draw}W"
        except Exception as e:
            return f"❌ Error creating device: {str(e)}"

    result = await create()
    return [TextContent(type="text", text=result)]


async def create_rack(arguments: dict) -> list[TextContent]:
    """Create a new rack in a site"""

    @sync_to_async
    def create():
        try:
            site_name = arguments.get("site_name")
            rack_name = arguments.get("rack_name")

            try:
                site = Site.objects.get(name=site_name)
            except Site.DoesNotExist:
                return f"❌ Site '{site_name}' not found."

            # Check if rack already exists
            if Rack.objects.filter(site=site, name=rack_name).exists():
                return f"❌ Rack '{rack_name}' already exists in site '{site_name}'."

            rack = Rack.objects.create(
                site=site,
                name=rack_name,
                ru_height=arguments.get("ru_height", 42),
                description=arguments.get("description", ""),
            )
            return f"✅ Rack created successfully!\n\nSite: {site.name}\nRack: {rack.name}\nHeight: {rack.ru_height}U"
        except Exception as e:
            return f"❌ Error creating rack: {str(e)}"

    result = await create()
    return [TextContent(type="text", text=result)]


async def delete_rack(site_name: str, rack_name: str) -> list[TextContent]:
    """Delete a rack from a site"""

    @sync_to_async
    def delete():
        try:
            try:
                site = Site.objects.get(name=site_name)
                rack = Rack.objects.get(site=site, name=rack_name)
            except Site.DoesNotExist:
                return f"❌ Site '{site_name}' not found."
            except Rack.DoesNotExist:
                return f"❌ Rack '{rack_name}' not found in site '{site_name}'."

            # Check if rack has devices
            device_count = rack.rack_devices.count()
            if device_count > 0:
                return f"❌ Cannot delete rack '{rack_name}': it contains {device_count} device(s). Remove all devices first."

            rack.delete()
            return f"✅ Rack '{rack_name}' deleted successfully from site '{site_name}'."
        except Exception as e:
            return f"❌ Error deleting rack: {str(e)}"

    result = await delete()
    return [TextContent(type="text", text=result)]


async def update_site_name(old_name: str, new_name: str) -> list[TextContent]:
    """Update a site's name"""

    @sync_to_async
    def update():
        try:
            try:
                site = Site.objects.get(name=old_name)
            except Site.DoesNotExist:
                return f"❌ Site '{old_name}' not found."

            # Check if new name already exists
            if Site.objects.filter(name=new_name).exclude(id=site.id).exists():
                return f"❌ A site named '{new_name}' already exists."

            old = site.name
            site.name = new_name
            site.save()
            return f"✅ Site name updated successfully!\n\nOld name: {old}\nNew name: {site.name}"
        except Exception as e:
            return f"❌ Error updating site name: {str(e)}"

    result = await update()
    return [TextContent(type="text", text=result)]


async def create_device_group(arguments: dict) -> list[TextContent]:
    """Create a new device group"""

    @sync_to_async
    def create():
        try:
            name = arguments.get("name")

            if DeviceGroup.objects.filter(name=name).exists():
                return f"❌ Device group '{name}' already exists."

            device_group = DeviceGroup.objects.create(name=name, description=arguments.get("description", ""))
            return f"✅ Device group created successfully!\n\nName: {device_group.name}\nDescription: {device_group.description or 'N/A'}"
        except Exception as e:
            return f"❌ Error creating device group: {str(e)}"

    result = await create()
    return [TextContent(type="text", text=result)]


async def create_provider(arguments: dict) -> list[TextContent]:
    """Create a new hardware provider"""

    @sync_to_async
    def create():
        try:
            name = arguments.get("name")

            if Provider.objects.filter(name=name).exists():
                return f"❌ Provider '{name}' already exists."

            provider = Provider.objects.create(
                name=name, description=arguments.get("description", ""), website=arguments.get("website", "")
            )
            return f"✅ Provider created successfully!\n\nName: {provider.name}\nWebsite: {provider.website or 'N/A'}\nDescription: {provider.description or 'N/A'}"
        except Exception as e:
            return f"❌ Error creating provider: {str(e)}"

    result = await create()
    return [TextContent(type="text", text=result)]


async def main_stdio():
    """Run MCP server with stdio transport"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


async def handle_mcp_request(request):
    """Handle HTTP MCP requests"""
    try:
        body = await request.json()
        method = body.get("method")
        params = body.get("params", {})

        if method == "tools/list":
            tools = await list_tools()
            result = [{"name": t.name, "description": t.description, "inputSchema": t.inputSchema} for t in tools]
            return Response(content=json.dumps({"result": result}), media_type="application/json")
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            result = await call_tool(tool_name, arguments)
            return Response(
                content=json.dumps({"result": [{"type": r.type, "text": r.text} for r in result]}),
                media_type="application/json",
            )
        else:
            return Response(
                content=json.dumps({"error": f"Unknown method: {method}"}),
                media_type="application/json",
                status_code=400,
            )
    except Exception as e:
        return Response(content=json.dumps({"error": str(e)}), media_type="application/json", status_code=500)


def create_http_app():
    """Create Starlette app for HTTP transport"""
    routes = [Route("/mcp", handle_mcp_request, methods=["POST"])]
    return Starlette(debug=True, routes=routes)


async def main_http(port: int):
    """Run MCP server with HTTP transport"""
    config = uvicorn.Config(create_http_app(), host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MCP Server for RackSum")
    parser.add_argument(
        "--transport", choices=["stdio", "http"], default="stdio", help="Transport protocol to use (default: stdio)"
    )
    parser.add_argument("--port", type=int, default=3001, help="Port for HTTP transport (default: 3001)")
    args = parser.parse_args()

    if args.transport == "http":
        print(f"Starting MCP server with HTTP transport on port {args.port}...")
        asyncio.run(main_http(args.port))
    else:
        print("Starting MCP server with stdio transport...")
        asyncio.run(main_stdio())
