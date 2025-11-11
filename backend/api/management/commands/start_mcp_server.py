"""
Django management command to start the MCP server
"""

import sys
import os
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Start the MCP server for Claude integration"

    def handle(self, *args, **options):
        if not settings.MCP_ENABLED:
            self.stdout.write(self.style.WARNING("MCP server is disabled. Set MCP_ENABLED=true in .env to enable it."))
            return

        self.stdout.write(self.style.SUCCESS(f"Starting MCP server on port {settings.MCP_PORT}..."))

        # Import and run the MCP server
        try:
            # Add backend directory to path
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            if backend_dir not in sys.path:
                sys.path.insert(0, backend_dir)

            # Import and run the server
            from mcp_server import main
            import asyncio

            self.stdout.write(self.style.SUCCESS("MCP server started successfully. Available tools:"))
            self.stdout.write("  - get_site_stats: Get statistics for all sites")
            self.stdout.write("  - get_site_details: Get detailed info about a specific site")
            self.stdout.write("  - get_rack_details: Get detailed info about a specific rack")
            self.stdout.write("  - get_available_resources: List available device types")
            self.stdout.write("  - get_resource_summary: Get overall resource utilization summary")
            self.stdout.write("")

            asyncio.run(main())

        except ImportError as e:
            self.stdout.write(self.style.ERROR(f"Failed to import MCP server module: {e}"))
            self.stdout.write(self.style.WARNING("Make sure the mcp package is installed: pip install mcp"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error starting MCP server: {e}"))
