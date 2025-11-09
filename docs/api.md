# API Reference

RackSum provides a REST API for programmatic access to configuration management. This allows integration with external tools, automation workflows, and custom applications.

## Base URL

```
http://localhost:3000/api
```

For production deployments, replace `localhost:3000` with your server's address.

## Authentication

Currently, the API does not require authentication. For production deployments, consider implementing:

- API keys
- OAuth 2.0
- JWT tokens
- Basic authentication

## Endpoints

### Load Configuration

Load a rack configuration into RackSum.

**Endpoint:** `POST /api/load`

**Content-Type:** `application/json`

**Request Body:**

```json
{
  "configId": "unique-id",
  "metadata": {
    "createdAt": "2024-01-15T10:30:00Z",
    "lastModified": "2024-01-15T14:22:00Z",
    "description": "Production Datacenter Layout"
  },
  "settings": {
    "totalPowerCapacity": 10000,
    "hvacCapacity": 34100,
    "ruPerRack": 42
  },
  "racks": [
    {
      "id": "rack-1",
      "name": "Rack A1",
      "devices": []
    }
  ],
  "unrackedDevices": [],
  "devices": []
}
```

**Response:**

```json
{
  "success": true,
  "message": "Configuration loaded successfully",
  "stats": {
    "racks": 4,
    "rackedDevices": 12,
    "unrackedDevices": 3,
    "totalPower": 8500,
    "totalHVAC": 12.1
  }
}
```

**Status Codes:**

- `200 OK`: Configuration loaded successfully
- `400 Bad Request`: Invalid JSON or missing required fields
- `500 Internal Server Error`: Server error

**Example:**

```bash
curl -X POST http://localhost:3000/api/load \
  -H "Content-Type: application/json" \
  -d '{
    "settings": {
      "totalPowerCapacity": 10000,
      "hvacCapacity": 10,
      "ruPerRack": 42
    },
    "racks": [
      {
        "id": "rack-1",
        "name": "Rack 1",
        "devices": []
      }
    ]
  }'
```

### Get Devices

Retrieve the device library.

**Endpoint:** `GET /api/devices`

**Response:**

```json
{
  "categories": [
    {
      "id": "network",
      "name": "Network Equipment",
      "devices": [
        {
          "id": "cisco-c9300-48p",
          "name": "Cisco Catalyst 9300 48-port",
          "category": "network",
          "ruSize": 1,
          "powerDraw": 750,
          "color": "#3498DB",
          "description": "48-port Gigabit switch"
        }
      ]
    }
  ]
}
```

**Status Codes:**

- `200 OK`: Devices retrieved successfully
- `500 Internal Server Error`: Server error

**Example:**

```bash
curl http://localhost:3000/api/devices
```

## Data Models

### Configuration Object

The complete configuration structure:

```typescript
interface Configuration {
  configId?: string;
  metadata?: {
    createdAt?: string;
    lastModified?: string;
    description?: string;
  };
  settings: {
    totalPowerCapacity: number;  // Watts
    hvacCapacity: number;         // Refrigeration Tons
    ruPerRack: number;            // Rack Units
  };
  racks: Rack[];
  unrackedDevices?: Device[];
  devices?: Device[];
}
```

### Rack Object

Individual rack definition:

```typescript
interface Rack {
  id: string;
  name: string;
  devices: DeviceInstance[];
}
```

### Device Object

Device template from library:

```typescript
interface Device {
  id: string;
  name: string;
  category: 'power' | 'network' | 'servers' | 'storage' | 'specialized';
  ruSize: number;           // Rack units (1, 2, 4, etc.)
  powerDraw: number;        // Watts
  color: string;            // Hex color code
  description?: string;
}
```

### Device Instance Object

Device placed in a rack or unracked:

```typescript
interface DeviceInstance extends Device {
  instanceId: string;
  customName?: string;
  position?: number;        // RU position in rack
  rackId?: string;          // Rack assignment
}
```

## Device Handling Logic

When POSTing configurations, devices are categorized into three groups:

### 1. Racked Devices

Devices with both `position` and `rackId` are placed directly in racks.

```json
{
  "racks": [
    {
      "id": "rack-1",
      "devices": [
        {
          "id": "cisco-c9300-48p",
          "name": "Cisco Catalyst 9300",
          "position": 1,
          "rackId": "rack-1",
          "powerDraw": 750,
          "ruSize": 1
        }
      ]
    }
  ]
}
```

### 2. Explicitly Unracked Devices

Devices in the `unrackedDevices` array appear in the Unracked Devices panel.

```json
{
  "unrackedDevices": [
    {
      "id": "dell-r750-2u",
      "name": "Dell PowerEdge R750",
      "powerDraw": 1400,
      "ruSize": 2,
      "instanceId": "server-spare-1"
    }
  ]
}
```

### 3. Auto-Unracked Devices

Devices in a top-level `devices` array without position data automatically go to Unracked Devices.

```json
{
  "devices": [
    {
      "id": "cisco-nexus-9k",
      "name": "Cisco Nexus 9000",
      "powerDraw": 500,
      "ruSize": 1
    }
  ]
}
```

**Use Case:** Import a device inventory from another system where positions haven't been assigned yet.

## Integration Examples

### Python Integration

```python
import requests
import json

# Load configuration
config = {
    "settings": {
        "totalPowerCapacity": 20000,
        "hvacCapacity": 20,
        "ruPerRack": 42
    },
    "racks": [
        {"id": "rack-1", "name": "Production Rack 1", "devices": []}
    ],
    "devices": [
        {
            "id": "dell-r750-2u",
            "name": "Dell R750 Server",
            "powerDraw": 1400,
            "ruSize": 2
        }
    ]
}

response = requests.post(
    'http://localhost:3000/api/load',
    json=config,
    headers={'Content-Type': 'application/json'}
)

if response.status_code == 200:
    print("Configuration loaded successfully")
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

### JavaScript/Node.js Integration

```javascript
const axios = require('axios');

async function loadConfiguration() {
  const config = {
    settings: {
      totalPowerCapacity: 20000,
      hvacCapacity: 20,
      ruPerRack: 42
    },
    racks: [
      { id: 'rack-1', name: 'Production Rack 1', devices: [] }
    ],
    devices: [
      {
        id: 'dell-r750-2u',
        name: 'Dell R750 Server',
        powerDraw: 1400,
        ruSize: 2
      }
    ]
  };

  try {
    const response = await axios.post(
      'http://localhost:3000/api/load',
      config
    );
    console.log('Success:', response.data);
  } catch (error) {
    console.error('Error:', error.message);
  }
}

loadConfiguration();
```

### Bash/cURL Integration

```bash
#!/bin/bash

# Create configuration file
cat > config.json <<EOF
{
  "settings": {
    "totalPowerCapacity": 20000,
    "hvacCapacity": 20,
    "ruPerRack": 42
  },
  "racks": [
    {
      "id": "rack-1",
      "name": "Production Rack 1",
      "devices": []
    }
  ],
  "devices": [
    {
      "id": "dell-r750-2u",
      "name": "Dell R750 Server",
      "powerDraw": 1400,
      "ruSize": 2
    }
  ]
}
EOF

# Load configuration
curl -X POST http://localhost:3000/api/load \
  -H "Content-Type: application/json" \
  -d @config.json

# Get device library
curl http://localhost:3000/api/devices | jq '.'
```

## Automation Workflows

### Automated Deployment Planning

```python
# Example: Generate RackSum config from infrastructure-as-code

import json

def generate_racksum_config(servers, switches, power_capacity):
    """Generate RackSum configuration from server inventory"""

    config = {
        "settings": {
            "totalPowerCapacity": power_capacity,
            "hvacCapacity": (power_capacity * 3.41) / 12000,  # Auto-calculate tons
            "ruPerRack": 42
        },
        "racks": [],
        "devices": []
    }

    # Add all servers as unracked devices
    for server in servers:
        config["devices"].append({
            "id": f"server-{server['model']}",
            "name": server['name'],
            "powerDraw": server['power'],
            "ruSize": server['ru_size'],
            "instanceId": server['serial']
        })

    # Add switches as unracked devices
    for switch in switches:
        config["devices"].append({
            "id": f"switch-{switch['model']}",
            "name": switch['name'],
            "powerDraw": switch['power'],
            "ruSize": 1,
            "instanceId": switch['serial']
        })

    return config

# Example usage
servers = [
    {"model": "r750", "name": "DB Server 1", "power": 1400, "ru_size": 2, "serial": "SN001"},
    {"model": "r750", "name": "DB Server 2", "power": 1400, "ru_size": 2, "serial": "SN002"}
]

switches = [
    {"model": "c9300", "name": "Core Switch", "power": 750, "serial": "SW001"}
]

config = generate_racksum_config(servers, switches, 20000)
print(json.dumps(config, indent=2))
```

### Capacity Monitoring

```python
# Example: Check if new equipment fits in existing capacity

def check_capacity(current_config, new_devices):
    """Check if new devices fit within capacity limits"""

    # Calculate current usage
    current_power = sum(d['powerDraw'] for d in current_config.get('devices', []))

    # Calculate new usage
    new_power = sum(d['powerDraw'] for d in new_devices)

    # Check against capacity
    total_capacity = current_config['settings']['totalPowerCapacity']
    total_power = current_power + new_power
    utilization = (total_power / total_capacity) * 100

    if utilization > 90:
        return {
            "fits": False,
            "message": f"Exceeds capacity: {utilization:.1f}%",
            "recommendation": "Increase power capacity or reduce equipment"
        }
    elif utilization > 70:
        return {
            "fits": True,
            "message": f"Warning: High utilization {utilization:.1f}%",
            "recommendation": "Consider capacity planning for future growth"
        }
    else:
        return {
            "fits": True,
            "message": f"Within capacity: {utilization:.1f}%",
            "recommendation": "Adequate headroom available"
        }
```

## Error Handling

### Common Error Responses

#### Invalid JSON

```json
{
  "success": false,
  "error": "Invalid JSON syntax",
  "details": "Unexpected token } in JSON at position 123"
}
```

#### Missing Required Fields

```json
{
  "success": false,
  "error": "Missing required field: settings",
  "details": "Configuration must include settings object"
}
```

#### Invalid Device ID

```json
{
  "success": false,
  "error": "Unknown device ID: invalid-device",
  "details": "Device not found in library"
}
```

### Error Handling Best Practices

1. **Validate Before Sending**
   - Check JSON syntax
   - Verify required fields
   - Validate data types

2. **Handle HTTP Errors**
   - Check response status codes
   - Parse error messages
   - Implement retry logic for network errors

3. **Log Errors**
   - Record failed requests
   - Track error patterns
   - Monitor API health

## Rate Limiting

Currently, no rate limiting is implemented. For production:

- Implement request throttling
- Add API key-based quotas
- Monitor for abuse patterns

## CORS Configuration

The API includes CORS headers for cross-origin requests. Allowed origins can be configured in the backend settings.

## Future API Enhancements

Planned additions:

- `GET /api/configurations` - List saved configurations
- `POST /api/configurations` - Save a configuration
- `GET /api/configurations/:id` - Get specific configuration
- `PUT /api/configurations/:id` - Update configuration
- `DELETE /api/configurations/:id` - Delete configuration
- `GET /api/statistics` - Get usage statistics
- `POST /api/validate` - Validate configuration without loading

## Support

For API issues or questions:

1. Check this documentation
2. Review error messages carefully
3. Verify JSON structure
4. Test with minimal examples first
5. Check server logs for details
