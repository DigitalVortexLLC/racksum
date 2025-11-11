# Swagger API Documentation

This document describes how to access and use the interactive Swagger/OpenAPI documentation for the RackSum API.

## Overview

The RackSum API now includes comprehensive **Swagger/OpenAPI 3.0** documentation powered by [drf-spectacular](https://drf-spectacular.readthedocs.io/). This provides:

- **Interactive API Explorer** - Test API endpoints directly from your browser
- **Detailed Request/Response Schemas** - See exactly what data each endpoint expects and returns
- **Authentication Support** - Test authenticated endpoints with your session
- **Code Examples** - View example requests and responses for each endpoint

## Accessing the Documentation

Once the Django server is running, you can access the API documentation at these URLs:

### Swagger UI (Recommended)
**URL:** `http://localhost:3000/api/docs/`

Swagger UI provides an interactive interface where you can:
- Browse all available endpoints organized by tags
- View detailed parameter and response information
- Execute API requests directly from the browser
- See example request/response payloads

### ReDoc (Alternative View)
**URL:** `http://localhost:3000/api/redoc/`

ReDoc provides a clean, three-panel documentation interface that's great for reading and reference.

### OpenAPI Schema (Raw)
**URL:** `http://localhost:3000/api/schema/`

Download the raw OpenAPI 3.0 schema in YAML or JSON format for use with code generators, testing tools, etc.

## Starting the Server

To access the documentation, start the Django development server:

```bash
# Navigate to the backend directory
cd backend

# Start the Django server
python manage.py runserver 3000
```

Then open your browser to:
- Swagger UI: http://localhost:3000/api/docs/
- ReDoc: http://localhost:3000/api/redoc/

## API Overview

The RackSum API provides the following endpoint groups:

### Sites
Manage datacenter site locations
- `GET /api/sites/` - List all sites
- `POST /api/sites/` - Create a new site
- `GET /api/sites/{id}/` - Get site details
- `PUT /api/sites/{id}/` - Update a site
- `DELETE /api/sites/{id}/` - Delete a site

### Devices
Manage device templates and types
- `GET /api/devices/` - List all devices
- `POST /api/devices/` - Create a new device
- `GET /api/devices/{id}/` - Get device details
- `PUT /api/devices/{id}/` - Update a device
- `DELETE /api/devices/{id}/` - Delete a device

### Racks
Manage rack configurations
- `GET /api/racks/` - List all racks (filter by `?site_id=`)
- `GET /api/racks/{id}/` - Get rack details with devices
- `PUT /api/racks/{id}/` - Update a rack
- `DELETE /api/racks/{id}/` - Delete a rack
- `POST /api/sites/{site_id}/create-rack` - Create a rack for a site

### Rack Devices
Manage device placements within racks
- `POST /api/racks/{rack_id}/add-device` - Add a device to a rack
- `DELETE /api/rack-devices/{rack_device_id}` - Remove a device from a rack

### Resource Usage
Calculate power and HVAC requirements
- `GET /api/sites/{site_id}/resource-usage` - Get total power/HVAC for a site
- `GET /api/racks/{rack_id}/resource-usage` - Get power/HVAC for a specific rack

### Authentication
WebAuthn/Passkey authentication endpoints
- `GET /api/auth/config` - Get authentication configuration
- `POST /api/auth/passkey/register/begin` - Start passkey registration
- `POST /api/auth/passkey/register/complete` - Complete passkey registration
- `POST /api/auth/passkey/login/begin` - Start passkey authentication
- `POST /api/auth/passkey/login/complete` - Complete passkey authentication
- `GET /api/auth/passkey/list` - List user's passkeys (requires auth)
- `DELETE /api/auth/passkey/{passkey_id}` - Delete a passkey (requires auth)
- `POST /api/auth/logout` - Logout (requires auth)
- `GET /api/auth/user` - Get current user (requires auth)

### Legacy Endpoints
Compatibility endpoints for migration from Express
- `GET /api/devices-json` - Get devices from JSON file
- `POST /api/load` - Load rack configuration
- `GET /api/rack-configs` - Get all rack configurations
- And more...

## Using the Swagger UI

### 1. Exploring Endpoints

- Endpoints are organized by **Tags** (Sites, Devices, Racks, etc.)
- Click on a tag to expand and see all endpoints in that category
- Click on an endpoint to see details

### 2. Viewing Request/Response Details

Each endpoint shows:
- **HTTP Method** and **Path**
- **Description** of what the endpoint does
- **Parameters** (path, query, request body)
- **Request Body Schema** with examples
- **Response Schemas** for different status codes
- **Example Responses**

### 3. Testing Endpoints (Try it out)

1. Click on an endpoint to expand it
2. Click the **"Try it out"** button
3. Fill in any required parameters
4. Edit the request body if needed
5. Click **"Execute"**
6. View the response (status code, headers, body)

### 4. Authentication

Some endpoints require authentication:
- First, authenticate using the passkey endpoints
- Your session will be maintained in the browser
- Authenticated endpoints will work automatically

## Configuration

The Swagger documentation is configured in `/backend/backend/settings.py`:

```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'RackSum API',
    'DESCRIPTION': 'Datacenter Rack Management API',
    'VERSION': '1.0.0',
    'TAGS': [
        {'name': 'Sites', 'description': 'Physical datacenter site management'},
        {'name': 'Devices', 'description': 'Device template and type management'},
        # ... more tags
    ],
}
```

## Generating the Schema

To generate or update the OpenAPI schema file:

```bash
cd backend
python manage.py spectacular --color --file schema.yml
```

This creates a `schema.yml` file that can be:
- Imported into API testing tools (Postman, Insomnia, etc.)
- Used with code generators to create API clients
- Shared with frontend developers
- Validated with OpenAPI tools

## Benefits of Swagger Documentation

1. **Interactive Testing** - Test all endpoints without writing code
2. **Clear Contracts** - See exactly what data is expected and returned
3. **Live Documentation** - Always up-to-date with the code
4. **Developer Onboarding** - New developers can explore the API immediately
5. **API Client Generation** - Generate client libraries in multiple languages
6. **Integration Testing** - Import schema into testing tools

## Additional Resources

- [Swagger UI Documentation](https://swagger.io/tools/swagger-ui/)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [drf-spectacular Documentation](https://drf-spectacular.readthedocs.io/)
- [ReDoc Documentation](https://redocly.com/docs/redoc/)

## Troubleshooting

### Documentation not loading
- Ensure the Django server is running
- Check that drf-spectacular is installed: `pip install drf-spectacular`
- Verify `drf_spectacular` is in `INSTALLED_APPS` in settings.py

### Missing endpoints
- Run `python manage.py spectacular` to see any schema generation warnings
- Add `@extend_schema()` decorators to function-based views
- Ensure serializers are properly configured for ViewSets

### Authentication not working
- Authenticate via the passkey endpoints first
- Ensure cookies are enabled in your browser
- Check CORS settings if accessing from a different origin

## Contributing

When adding new API endpoints:

1. Add appropriate `@extend_schema()` decorators with:
   - `summary` - Short description
   - `description` - Detailed explanation
   - `tags` - Relevant category
   - `examples` - Request/response examples
   - `parameters` - Path/query parameters

2. Update serializers with proper field descriptions

3. Regenerate the schema: `python manage.py spectacular --file schema.yml`

4. Test the documentation in Swagger UI

This ensures the documentation stays accurate and helpful!
