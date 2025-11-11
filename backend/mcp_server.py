"""
MCP Server for RackSum - Entry point with HTTP and stdio transport support

This file provides both stdio and HTTP transport modes for the MCP server.
The actual implementation is modularized into the mcp package.
"""

import argparse
import asyncio
from mcp.server import main_stdio, main_http

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
