# MCP Server Integration

Racker includes an optional Model Context Protocol (MCP) server that allows AI assistants like Claude to access site statistics and resource information directly.

## Overview

The MCP server provides a programmatic interface for AI assistants to:
- Query site statistics and rack configurations
- Get real-time resource utilization data (power, HVAC)
- List available device types and specifications
- Generate resource summaries across all sites

## Configuration

### Enabling the MCP Server

1. Create a `.env` file in the project root (or copy from `.env.example`)
2. Add the following configuration:

```bash
# MCP Server Configuration
MCP_ENABLED=true
MCP_PORT=3001
```

### Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `MCP_ENABLED` | Enable/disable the MCP server | `false` |
| `MCP_PORT` | Port for the MCP server (not used in stdio mode) | `3001` |

## Starting the MCP Server

### Automatic Startup (Recommended)

When `MCP_ENABLED=true`, the MCP server starts automatically when you run:

```bash
./start_server.sh
```

The server runs in a background thread alongside Django, using stdio for communication.

### Manual Startup

You can also start the MCP server manually using Django's management command:

```bash
cd backend
source ../venv/bin/activate
python manage.py start_mcp_server
```

## Available Tools

The MCP server provides the following tools:

### 1. get_site_stats

Get statistics for all sites in the system.

**Parameters:** None

**Returns:** List of all sites with:
- Number of racks
- Total devices
- Power consumption (W/kW)
- HVAC load (BTU/hr, tons)

**Example Output:**
```
=== SITE STATISTICS ===

📍 Site: Main Datacenter
   Racks: 5
   Devices: 47
   Total Power: 12,450 W (12.45 kW)
   Total HVAC Load: 42,454 BTU/hr (3.54 tons)
   Created: 2025-01-15 10:30
```

### 2. get_site_details

Get detailed information about a specific site.

**Parameters:**
- `site_name` (string, required): Name of the site

**Returns:** Detailed site information including:
- Site description and metadata
- List of all racks with usage statistics
- Space utilization per rack
- Power and HVAC loads per rack

**Example:**
```json
{
  "site_name": "Main Datacenter"
}
```

### 3. get_rack_details

Get detailed information about a specific rack.

**Parameters:**
- `site_name` (string, required): Name of the site
- `rack_name` (string, required): Name of the rack

**Returns:** Detailed rack information including:
- Rack dimensions and capacity
- Space utilization (RU used/available)
- Complete device inventory
- Power and HVAC calculations
- Device positions and specifications

**Example:**
```json
{
  "site_name": "Main Datacenter",
  "rack_name": "Rack-A1"
}
```

### 4. get_available_resources

List all available device types and their specifications.

**Parameters:**
- `category` (string, optional): Filter by device category (case-insensitive)
- `limit` (integer, optional): Maximum number of devices to return (useful for large device catalogs)

**Returns:** Grouped list of device types with:
- Device name and ID
- Category
- Physical size (RU)
- Power consumption
- Heat output
- Display color
- Pagination info if results were limited

**Example:**
```json
{
  "category": "Server",
  "limit": 10
}
```

### 5. get_resource_summary

Get overall resource utilization summary across all sites.

**Parameters:** None

**Returns:** System-wide summary including:
- Total counts (sites, racks, devices)
- Overall capacity metrics
- Total power consumption
- Total HVAC requirements
- Average utilization statistics

## Features

### Performance Optimizations
- **Efficient Database Queries**: Uses Django's `prefetch_related()` to eliminate N+1 query problems
- **Optimized for Scale**: Can handle large datacenters with hundreds of racks and thousands of devices

### User-Friendly Design
- **Case-Insensitive Lookups**: Site and rack names are matched case-insensitively for better user experience
- **Pagination Support**: Optional limit parameter for device listings to handle large catalogs
- **Comprehensive Error Handling**: Detailed error messages and logging for troubleshooting

### Configurable Constants
- **WATTS_TO_BTU**: Configurable conversion factor (default: 3.412) for power-to-heat calculations
- **BTU_PER_TON**: Configurable HVAC constant (default: 12,000) for cooling capacity calculations

## Using with Claude

### Claude Desktop Configuration

Add the MCP server to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "racksum": {
      "command": "python",
      "args": [
        "/path/to/racksum/backend/manage.py",
        "start_mcp_server"
      ],
      "env": {
        "DJANGO_SETTINGS_MODULE": "backend.settings",
        "MCP_ENABLED": "true"
      }
    }
  }
}
```

### Example Claude Queries

Once configured, you can ask Claude:

- "What sites do we have and what's their power usage?"
- "Show me the details of Rack-A1 in the Main Datacenter" (case-insensitive)
- "Show me details for rack-a1 in the main datacenter" (works with any case)
- "What device types are available in the server category?"
- "List the first 10 network devices" (uses pagination)
- "Give me a resource utilization summary across all sites"
- "How much HVAC capacity do I need for my datacenters?"

## Troubleshooting

### MCP Server Not Starting

1. **Check if MCP is enabled:**
   ```bash
   grep MCP_ENABLED .env
   ```
   Should return `MCP_ENABLED=true`

2. **Verify MCP package is installed:**
   ```bash
   source venv/bin/activate
   pip list | grep mcp
   ```
   If not installed:
   ```bash
   pip install mcp==1.1.2
   ```

3. **Check Django logs:**
   Look for `[MCP]` prefixed messages in the Django startup output

### No Data Returned

If tools return empty results:

1. **Verify database has data:**
   ```bash
   cd backend
   python manage.py shell
   ```
   ```python
   from api.models import Site, Rack, Device
   print(f"Sites: {Site.objects.count()}")
   print(f"Racks: {Rack.objects.count()}")
   print(f"Devices: {Device.objects.count()}")
   ```

2. **Check Django admin panel:**
   Visit `http://localhost:3000/admin` to verify data exists

## Security Considerations

- The MCP server runs with the same permissions as the Django application
- It has full read access to the database
- Currently configured for local use only (stdio transport)
- For production use, consider:
  - Adding authentication to MCP tools
  - Implementing rate limiting
  - Restricting data access based on user roles
  - Using secure transport mechanisms

## Technical Details

### Architecture

```
┌─────────────┐
│   Claude    │
│   Desktop   │
└──────┬──────┘
       │ stdio
       ▼
┌─────────────┐
│ MCP Server  │ (Python/asyncio)
│  (Thread)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Django    │
│  Database   │
└─────────────┘
```

### Implementation Files

The MCP server uses a modular architecture for better maintainability:

- `/backend/mcp/` - MCP server package directory
  - `server.py` - Main server entry point and request router
  - `tools.py` - Tool definitions and schemas
  - `handlers.py` - Tool handler implementations
  - `formatters.py` - Output formatting helper functions
- `/backend/mcp_server.py` - Backward compatibility wrapper
- `/backend/api/apps.py` - Django AppConfig with auto-start logic
- `/backend/api/management/commands/start_mcp_server.py` - Management command
- `/requirements.txt` - Dependencies (includes `mcp==1.1.2`)

**Modular Design Benefits:**
- **Separation of Concerns**: Each module has a single, well-defined responsibility
- **Testability**: Individual modules can be tested in isolation
- **Maintainability**: Changes to one aspect (e.g., formatting) don't affect others
- **Reusability**: Formatters and utilities can be reused across handlers
- **Readability**: Smaller, focused files are easier to understand and navigate

### Testing

The MCP server includes comprehensive test coverage:

- `/backend/mcp/tests/` - Test suite directory
  - `test_formatters.py` - Tests for formatting functions (18 tests)
  - `test_tools.py` - Tests for tool definitions (15 tests)
  - `test_handlers.py` - Tests for handler implementations (22 tests)
- `/backend/pytest.ini` - Pytest configuration

**Running Tests:**

```bash
# Run all MCP tests
cd backend
pytest mcp/tests/ -v

# Run with coverage
pytest mcp/tests/ -v --cov=mcp --cov-report=term-missing

# Run specific test file
pytest mcp/tests/test_formatters.py -v

# Run specific test
pytest mcp/tests/test_formatters.py::TestFormatters::test_format_power_basic -v
```

**Test Coverage:**
- 55+ test cases covering all MCP functionality
- Unit tests for formatters (pure functions)
- Integration tests for handlers (database operations)
- Parametrized tests for edge cases
- Async test support with pytest-asyncio
- Tests run automatically in CI/CD pipeline

**Continuous Integration:**
- Tests run on every push and pull request
- Tested against Python 3.10, 3.11, and 3.12
- MySQL database integration tests
- Code coverage reporting

### Dependencies

- **mcp**: Model Context Protocol Python SDK
- **Django**: Web framework and ORM
- **asyncio**: Async/await support for MCP server

## Related Documentation

- [API Documentation](api.md) - REST API endpoints
- [Configuration Guide](configuration.md) - Environment variables
- [Development Guide](development.md) - Development setup

## Support

For issues or questions:
- Check the [GitHub Issues](https://github.com/DigitalVortexLLC/racksum/issues)
- Review Django logs for error messages
- Ensure all dependencies are installed correctly
