"""
MCP Server for RackSum - Main entry point

Provides site stats and resource information through the Model Context Protocol.
This server exposes datacenter infrastructure data to AI assistants like Claude.
"""
import os
import sys
import django
import asyncio
import logging
from mcp.server import Server
from mcp.types import TextContent
from mcp.server.stdio import stdio_server

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from .tools import get_tool_definitions
from . import handlers

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='[MCP] %(asctime)s - %(levelname)s - %(message)s'
)

# Create MCP server instance
app = Server("racksum-stats")


@app.list_tools()
async def list_tools():
    """List available MCP tools"""
    return get_tool_definitions()


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Route tool calls to appropriate handlers"""

    # Extract output_format, default to "text" for backward compatibility
    output_format = arguments.get("output_format", "text")

    if name == "get_site_stats":
        return await handlers.get_site_stats(output_format)

    elif name == "get_site_details":
        site_name = arguments.get("site_name")
        if not site_name:
            return [TextContent(type="text", text="Error: site_name is required")]
        return await handlers.get_site_details(site_name, output_format)

    elif name == "get_rack_details":
        site_name = arguments.get("site_name")
        rack_name = arguments.get("rack_name")
        if not site_name or not rack_name:
            return [TextContent(type="text", text="Error: site_name and rack_name are required")]
        return await handlers.get_rack_details(site_name, rack_name, output_format)

    elif name == "get_available_resources":
        category = arguments.get("category")
        limit = arguments.get("limit")
        return await handlers.get_available_resources(category, limit, output_format)

    elif name == "get_resource_summary":
        return await handlers.get_resource_summary(output_format)

    elif name == "create_device":
        return await handlers.create_device(arguments)

    elif name == "create_rack":
        return await handlers.create_rack(arguments)

    elif name == "delete_rack":
        site_name = arguments.get("site_name")
        rack_name = arguments.get("rack_name")
        if not site_name or not rack_name:
            return [TextContent(type="text", text="Error: site_name and rack_name are required")]
        return await handlers.delete_rack(site_name, rack_name)

    elif name == "update_site_name":
        old_name = arguments.get("old_name")
        new_name = arguments.get("new_name")
        if not old_name or not new_name:
            return [TextContent(type="text", text="Error: old_name and new_name are required")]
        return await handlers.update_site_name(old_name, new_name)

    elif name == "create_device_group":
        return await handlers.create_device_group(arguments)

    elif name == "create_provider":
        return await handlers.create_provider(arguments)

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main_stdio():
    """Run MCP server with stdio transport"""
    logger.info("Starting RackSum MCP server with stdio transport...")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


async def handle_mcp_request(request):
    """Handle HTTP MCP requests"""
    import json
    from starlette.responses import Response

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
        logger.error(f"Error handling MCP request: {e}", exc_info=True)
        return Response(content=json.dumps({"error": str(e)}), media_type="application/json", status_code=500)


def create_http_app():
    """Create Starlette app for HTTP transport"""
    from starlette.applications import Starlette
    from starlette.routing import Route

    routes = [Route("/mcp", handle_mcp_request, methods=["POST"])]
    return Starlette(debug=True, routes=routes)


async def main_http(port: int):
    """Run MCP server with HTTP transport"""
    import uvicorn

    logger.info(f"Starting RackSum MCP server with HTTP transport on port {port}...")
    config = uvicorn.Config(create_http_app(), host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main_stdio())
