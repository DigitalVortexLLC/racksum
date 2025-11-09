# Racksum API Documentation

## Base URL
`http://localhost:3000`

## Authentication
Currently, the API doesn't require authentication for most endpoints. The Django Admin interface requires login.

## Admin Access
- **URL**: `http://localhost:3000/admin/`
- **Username**: `admin`
- **Password**: `admin123`

## API Endpoints

### Root
- **GET** `/` - API documentation and available endpoints

### Sites

#### List all sites
```
GET /api/sites/
```

#### Create a site
```
POST /api/sites/
Content-Type: application/json

{
  "name": "Datacenter A",
  "description": "Main datacenter location"
}
```

#### Get site details
```
GET /api/sites/{id}/
```

#### Update site
```
PUT /api/sites/{id}/
Content-Type: application/json

{
  "name": "Updated Datacenter A",
  "description": "Updated description"
}
```

#### Delete site
```
DELETE /api/sites/{id}/
```

#### Get site resource usage
```
GET /api/sites/{site_id}/resource-usage
```

**Response:**
```json
{
  "site_id": 1,
  "site_name": "Datacenter A",
  "total_power_draw": 4500,
  "total_hvac_load": 15345.0,
  "rack_count": 2,
  "racks": [
    {
      "id": 1,
      "name": "Rack A1",
      "power_draw": 2300,
      "hvac_load": 7843.0,
      "device_count": 3
    }
  ]
}
```

### Devices

#### List all devices
```
GET /api/devices/
```

#### Create a device
```
POST /api/devices/
Content-Type: application/json

{
  "device_id": "dell-r750",
  "name": "Dell PowerEdge R750",
  "category": "servers",
  "ru_size": 2,
  "power_draw": 1400,
  "color": "#8E44AD",
  "description": "2U dual-socket server"
}
```

**Fields:**
- `device_id` (string, required, unique): Unique identifier for the device
- `name` (string, required): Display name
- `category` (string, required): Device category (e.g., "servers", "network", "storage")
- `ru_size` (integer, required): Number of rack units (0 or greater)
- `power_draw` (integer, required): Power consumption in watts
- `color` (string, optional): Hex color code for display (default: "#000000")
- `description` (string, optional): Device description

#### Get device details
```
GET /api/devices/{id}/
```

#### Update device
```
PUT /api/devices/{id}/
Content-Type: application/json

{
  "device_id": "dell-r750",
  "name": "Dell PowerEdge R750 Updated",
  "category": "servers",
  "ru_size": 2,
  "power_draw": 1400,
  "color": "#8E44AD",
  "description": "Updated description"
}
```

#### Delete device
```
DELETE /api/devices/{id}/
```

### Racks

#### List all racks
```
GET /api/racks/

# Filter by site
GET /api/racks/?site_id={site_id}
```

#### Create a rack for a site
```
POST /api/sites/{site_id}/create-rack
Content-Type: application/json

{
  "name": "Rack A1",
  "ru_height": 42,
  "description": "Production rack"
}
```

**Fields:**
- `name` (string, required): Rack name
- `ru_height` (integer, optional): Rack height in units (default: 42)
- `description` (string, optional): Rack description

#### Get rack details
```
GET /api/racks/{id}/
```

**Response includes:**
- All rack information
- List of devices with positions
- Power utilization (watts)
- HVAC load (BTU/hr)

#### Update rack
```
PUT /api/racks/{id}/
Content-Type: application/json

{
  "name": "Updated Rack A1",
  "ru_height": 42,
  "description": "Updated description"
}
```

#### Delete rack
```
DELETE /api/racks/{id}/
```

#### Get rack resource usage
```
GET /api/racks/{rack_id}/resource-usage
```

**Response:**
```json
{
  "rack_id": 1,
  "rack_name": "Rack A1",
  "site_name": "Datacenter A",
  "total_power_draw": 2300,
  "total_hvac_load": 7843.0,
  "ru_height": 42,
  "devices": [
    {
      "id": 1,
      "device_name": "ESXi Host 1",
      "position": 10,
      "ru_size": 2,
      "power_draw": 1400,
      "hvac_load": 4774.0
    }
  ]
}
```

### Device Placement

#### Add device to rack
```
POST /api/racks/{rack_id}/add-device
Content-Type: application/json

{
  "device": 1,
  "position": 10,
  "instance_name": "ESXi Host 1"
}
```

**Fields:**
- `device` (integer, required): Device ID to place
- `position` (integer, required): Starting RU position (1-based)
- `instance_name` (string, optional): Custom name for this device instance

**Validation:**
- Device must fit within rack height
- Position must not conflict with existing devices
- Position is based on the starting RU (e.g., position 10 means RU 10)

#### Remove device from rack
```
DELETE /api/rack-devices/{rack_device_id}/
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Validation error message"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 409 Conflict
```json
{
  "error": "A resource with this identifier already exists"
}
```

### 500 Internal Server Error
```json
{
  "error": "Error message",
  "details": "Detailed error information"
}
```

## Django Admin

Access the Django Admin interface at `http://localhost:3000/admin/` to:

- View and manage all sites, devices, racks, and device placements
- See calculated resource usage (power and HVAC) for racks
- Filter and search across all models
- Bulk operations on multiple records

### Admin Features

**Sites Admin:**
- List view with name, description, and timestamps
- Search by name or description
- Filter by creation/update date

**Devices Admin:**
- List view with device ID, name, category, specifications
- Filter by category and dates
- Search by device ID, name, category, or description
- Color preview in list

**Racks Admin:**
- List view with rack name, site, height, device count, and power usage
- Filter by site and dates
- Search by rack name or site name
- View calculated power draw and HVAC load

**Rack Devices Admin:**
- List view with rack, device, position, and resource usage
- Filter by site, rack, and device category
- Search by rack name, device name, or instance name
- View calculated power draw and HVAC load for each device

## Example Workflow

### 1. Create a Site
```bash
curl -X POST http://localhost:3000/api/sites/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Datacenter A",
    "description": "Main datacenter"
  }'
```

### 2. Create Devices
```bash
curl -X POST http://localhost:3000/api/devices/ \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "dell-r750",
    "name": "Dell PowerEdge R750",
    "category": "servers",
    "ru_size": 2,
    "power_draw": 1400,
    "color": "#8E44AD"
  }'
```

### 3. Create a Rack
```bash
curl -X POST http://localhost:3000/api/sites/1/create-rack \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rack A1",
    "ru_height": 42
  }'
```

### 4. Add Device to Rack
```bash
curl -X POST http://localhost:3000/api/racks/1/add-device \
  -H "Content-Type: application/json" \
  -d '{
    "device": 1,
    "position": 10,
    "instance_name": "ESXi Host 1"
  }'
```

### 5. Get Resource Usage
```bash
curl http://localhost:3000/api/sites/1/resource-usage
```

## Notes

- All timestamps are in UTC
- Power draw is measured in watts (W)
- HVAC load is calculated as: power_draw × 3.41 (BTU/hr)
- RU positions are 1-based (position 1 is the bottom of the rack)
- Device placement validates against rack capacity and conflicts
