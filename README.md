# Racker - Rack Diagram Planning Tool

A web-based tool for planning and visualizing server rack layouts with real-time power and HVAC capacity tracking.

## Features

- **Interactive Rack Visualization**: Drag and drop devices into rack positions
- **Device Library**: Pre-configured devices organized by category (Power, Network, Servers, Storage, Specialized)
- **Unracked Devices Panel**: Temporary holding area for devices without rack assignments
- **Multi-Rack Support**: Configure and manage multiple racks
- **Real-Time Calculations**:
  - Power consumption tracking (includes unracked devices)
  - HVAC heat load calculation (1W = 3.41 BTU/hr)
  - Color-coded utilization warnings
- **Import/Export**: Save and load rack configurations as JSON
- **Persistent Storage**: Configurations automatically saved to browser localStorage
- **REST API**: POST endpoint to programmatically load configurations with automatic unracked device handling

## Tech Stack

- **Frontend**: Vue 3 (Composition API) + Vite
- **Styling**: Tailwind CSS
- **Backend**: Django + Django REST Framework
- **Database**: MySQL
- **Drag & Drop**: VueUse composables

## Installation

### Prerequisites

- Node.js (v20 or higher)
- npm
- Python 3.8 or higher
- MySQL server

### Setup

1. Clone or navigate to the project directory:
```bash
cd racker
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Set up Python virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env to set your MySQL database credentials
```

5. Run database migrations:
```bash
npm run db:init
```

## Development

Run the development server with hot-reload:

```bash
npm run dev
```

The application will be available at [http://localhost:5173](http://localhost:5173)

## Production

### Build and Run

1. Build the Vue application:
```bash
npm run build
```

2. Start the Django server:
```bash
npm run server
```

Or use the combined command:
```bash
npm start
```

The application will be available at [http://localhost:3000](http://localhost:3000)

**Note**: Make sure your Python virtual environment is activated before running the server.

## Usage

### Basic Workflow

1. **Configure Your Environment**:
   - Click "Configure" button
   - Set number of racks, RU per rack, power capacity, and HVAC capacity
   - Click "Save"

2. **Add Devices**:
   - Browse the device library on the left sidebar
   - Drag a device from the library
   - Drop it into a rack at your desired position
   - Devices automatically snap to RU boundaries

3. **Unracked Devices** (Right Panel):
   - Devices without rack assignments appear in the "Unracked Devices" panel
   - Useful when importing configurations via POST API without position data
   - Drag devices from this panel into racks to assign positions
   - View power consumption of unracked devices in utilization stats

4. **Monitor Resources**:
   - View real-time power and HVAC utilization in the bottom-right panel
   - Color indicators: Green (<70%), Yellow (70-90%), Red (>90%)

4. **Save/Load Configurations**:
   - Click "Import/Export" button
   - Export: Copy JSON or download as file
   - Import: Paste JSON or upload a file

### API Usage

Load a configuration programmatically via POST:

```bash
curl -X POST http://localhost:3000/api/load \
  -H "Content-Type: application/json" \
  -d @your-config.json
```

**Automatic Unracked Device Handling**: When POSTing configurations, devices can be handled in three ways:
1. **In Racks**: Devices with `position` and `rackId` are placed directly in racks
2. **Explicitly Unracked**: Devices in the `unrackedDevices` array appear in the Unracked Devices panel
3. **Auto-Unracked**: Devices in a top-level `devices` array without position data automatically go to Unracked Devices

This makes it easy to import device lists where rack positions haven't been determined yet!

## Configuration Format

### Rack Configuration JSON Schema

```json
{
  "configId": "unique-id",
  "metadata": {
    "createdAt": "2024-01-15T10:30:00Z",
    "lastModified": "2024-01-15T14:22:00Z",
    "description": "Optional description"
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
      "devices": [
        {
          "deviceId": "cisco-c9300-48p",
          "id": "cisco-c9300-48p",
          "name": "Cisco Catalyst 9300 48-port",
          "category": "network",
          "ruSize": 1,
          "powerDraw": 750,
          "color": "#3498DB",
          "position": 1,
          "instanceId": "switch-1",
          "customName": "Core Switch 1"
        }
      ]
    }
  ],
  "unrackedDevices": [
    {
      "id": "dell-r750-2u",
      "name": "Dell PowerEdge R750",
      "category": "servers",
      "ruSize": 2,
      "powerDraw": 1400,
      "color": "#8E44AD",
      "instanceId": "server-unassigned-1",
      "customName": "New Server - Needs Placement"
    }
  ],
  "devices": [
    {
      "id": "device-without-position",
      "name": "Some Device",
      "ruSize": 1,
      "powerDraw": 100
    }
  ]
}
```

### Device Definition Schema

```json
{
  "id": "unique-device-id",
  "name": "Device Name",
  "category": "network|power|servers|storage|specialized",
  "ruSize": 1,
  "powerDraw": 750,
  "color": "#3498DB",
  "description": "Device description"
}
```

## Adding Custom Devices

Edit `src/data/devices.json` to add your own devices:

```json
{
  "categories": [
    {
      "id": "custom",
      "name": "Custom Devices",
      "devices": [
        {
          "id": "my-device",
          "name": "My Custom Device",
          "category": "custom",
          "ruSize": 2,
          "powerDraw": 500,
          "color": "#FF5733",
          "description": "Custom device description"
        }
      ]
    }
  ]
}
```

## Calculations

### HVAC Heat Load
Heat load is calculated 1:1 with power draw, converted to BTU/hr:
```
Heat Load (BTU/hr) = Power Draw (W) × 3.41
```

### Utilization Percentage
```
Utilization % = (Used / Capacity) × 100
```

### Color Coding
- **Green**: < 70% capacity
- **Yellow**: 70-90% capacity
- **Red**: > 90% capacity

## Deployment

### Quick Deploy Options

1. **VPS/Cloud Server**: Copy files and run `npm start`
2. **Docker**: (Add Dockerfile if needed)
3. **Production WSGI Server** (recommended for production):
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
cd backend
gunicorn backend.wsgi:application --bind 0.0.0.0:3000
```

Alternatively, use the provided startup script:
```bash
chmod +x start_server.sh
./start_server.sh
```

## Project Structure

```
racker/
├── backend/             # Django backend
│   ├── manage.py       # Django management script
│   ├── backend/        # Django project settings
│   └── api/            # REST API app
│       ├── models.py   # Database models
│       ├── views.py    # API views
│       └── urls.py     # API routing
├── src/
│   ├── main.js         # Vue entry point
│   ├── App.vue         # Root component
│   ├── components/     # Vue components
│   ├── composables/    # State management
│   ├── data/          # Device library JSON
│   ├── utils/         # Utility functions
│   └── assets/        # Styles
├── public/            # Static assets
└── dist/              # Build output
```

## Troubleshooting

### Development server won't start
- Ensure port 5173 is not in use
- Check Node.js version: `node --version` (should be v20+)

### Production server issues
- Ensure you ran `npm run build` first
- Check that `dist/` directory exists
- Verify port 3000 is available
- Ensure Python virtual environment is activated
- Check Django is installed: `python -m django --version`
- Verify database connection in `.env` file

### Devices not loading
- Check browser console for errors
- Verify `src/data/devices.json` is valid JSON
- Check API endpoint: `http://localhost:3000/api/devices`
- Ensure Django server is running

### Database connection issues
- Verify MySQL server is running
- Check database credentials in `.env` file
- Ensure database exists: `mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS racker;"`
- Run migrations: `npm run db:init`

## License

ISC

## Support

For issues and questions, please refer to the documentation in [claude.md](claude.md) and [TODO.md](TODO.md).