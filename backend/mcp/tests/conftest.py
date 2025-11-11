"""
Pytest configuration for MCP tests

This conftest file ensures that 'mcp' package imports resolve to the installed
MCP SDK package, not the local mcp directory.
"""

import sys
import os

# Find and cache the installed mcp package before the local mcp directory shadows it
#
# The issue: When pytest runs from /home/user/racker/backend/, Python adds that directory
# to sys.path. This causes `import mcp` to find the local mcp/ directory instead of the
# installed mcp package from site-packages.
#
# The solution: Temporarily modify sys.path to remove the backend directory, clear any
# already-imported local mcp modules, import and cache specific modules from the installed
# mcp package, restore sys.path, then allow the local mcp package to be imported normally.

backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
backend_dir_abs = os.path.abspath(backend_dir)

# Clear any already-imported local mcp modules
# (except this conftest module itself)
if 'mcp' in sys.modules:
    modules_to_clear = [name for name in list(sys.modules.keys())
                       if (name == 'mcp' or name.startswith('mcp.'))
                       and not name.startswith('mcp.tests')]
    for name in modules_to_clear:
        del sys.modules[name]

# Save and modify sys.path to exclude backend directory
original_sys_path = sys.path.copy()
sys.path = [p for p in sys.path
            if os.path.abspath(p) != backend_dir_abs]

try:
    # Import from the installed mcp package (not the local directory)
    import mcp.types
    import mcp.server
    import mcp.server.stdio

    # Cache these modules so subsequent imports find them
    _mcp_types = mcp.types
    _mcp_server = mcp.server
    _mcp_server_stdio = mcp.server.stdio
    _installed_mcp = sys.modules['mcp']  # Also cache the main mcp module

except ImportError as e:
    # Restore sys.path before raising
    sys.path = original_sys_path
    raise ImportError(
        f"Could not import mcp package: {e}. "
        "Make sure mcp==1.1.2 is installed: pip install mcp==1.1.2"
    )

# Restore original sys.path
sys.path = original_sys_path

# Now remove the installed mcp from sys.modules so the local one can be imported
del sys.modules['mcp']
if 'mcp.types' in sys.modules:
    del sys.modules['mcp.types']
if 'mcp.server' in sys.modules:
    del sys.modules['mcp.server']
if 'mcp.server.stdio' in sys.modules:
    del sys.modules['mcp.server.stdio']

# Import the LOCAL mcp package (which contains formatters, handlers, tools, etc.)
# This will now be imported from the backend directory
import mcp  # noqa: F401

# NOW register the INSTALLED mcp submodules we cached
# This ensures `from mcp.types import X` finds the installed package modules
sys.modules["mcp.types"] = _mcp_types
sys.modules["mcp.server"] = _mcp_server
sys.modules["mcp.server.stdio"] = _mcp_server_stdio

# The local mcp package is registered as 'mcp' by the import above
# So now imports work as follows:
#   - `from mcp.types import X` -> finds the installed mcp.types (cached above)
#   - `from mcp.server import X` -> finds the installed mcp.server (cached above)
#   - `from mcp import handlers` -> finds the local mcp.handlers
#   - `from mcp.formatters import X` -> finds the local mcp.formatters
