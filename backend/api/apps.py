import os
import sys
import threading
from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
    mcp_server_started = False

    def ready(self):
        """
        Called when Django is ready. Start MCP server if enabled.
        """
        from django.conf import settings

        # Only start MCP server once and only if enabled
        # Also check if we're running the main server (not migrations, etc.)
        if settings.MCP_ENABLED and not ApiConfig.mcp_server_started and os.environ.get("RUN_MAIN") == "true":

            ApiConfig.mcp_server_started = True

            # Start MCP server in a separate thread
            thread = threading.Thread(target=self._start_mcp_server, daemon=True, name="MCP-Server")
            thread.start()

            print("[MCP] Server starting in background (stdio mode)...")
            print("[MCP] Use 'python manage.py start_mcp_server' to run in foreground")

    def _start_mcp_server(self):
        """Start the MCP server in a separate thread"""
        try:
            import asyncio
            from django.conf import settings

            # Add backend directory to path
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            if backend_dir not in sys.path:
                sys.path.insert(0, backend_dir)

            # Import and run MCP server
            from mcp_server import main

            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                loop.run_until_complete(main())
            except KeyboardInterrupt:
                print("[MCP] Server stopped")
            finally:
                loop.close()

        except Exception as e:
            print(f"[MCP] Error starting server: {e}")
            print("[MCP] Make sure 'mcp' package is installed: pip install mcp")
