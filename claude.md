# Rack Diagram Planning Tool

## Project Overview
A web-based tool for planning and visualizing server rack layouts with power and HVAC capacity tracking.

## Core Features

### 1. Rack Visualization
- **Standard Rack**: 42 RU (Rack Units) by default
- **Customizable**: User can configure number of racks and RU per rack
- **Visual Representation**:
  - Empty RU slots show as outlined rectangles
  - Occupied slots show filled colored rectangles
  - Devices can span multiple RUs based on their configuration

### 2. Device Library (Left Pane)
Accordion-based navigation with categorized devices:
- Power Equipment (UPS, PDU, etc.)
- Network Devices (Switches, Routers, Firewalls, etc.)
- Servers (1U, 2U, 4U servers, etc.)
- Storage (NAS, SAN, etc.)
- Additional categories as needed

#### Device Properties
Each device object contains:
- `name`: Device name/model
- `category`: Power/Network/Server/Storage/etc.
- `ruSize`: Number of RU units the device occupies
- `powerDraw`: Power consumption in watts
- `color`: Display color in the rack (hex code)
- `description`: Optional device description

### 3. Drag & Drop Interface
- Users can drag devices from the library
- Drop into specific RU positions in racks
- Devices snap to RU boundaries
- Visual feedback during drag operation
- Collision detection (can't place device if space occupied)

### 4. Configuration Menu
Settings for rack environment:
- **Number of Racks**: How many racks to display (1-N)
- **RU per Rack**: Rack height in units (default 42)
- **Total Power Capacity**: Available power in watts
- **HVAC Capacity**: Cooling capacity in BTU/hr or watts

### 5. Resource Utilization Display
Bottom-right legend showing:
- **Power Utilization**:
  - Bar graph showing used vs. available power
  - Color coding (green < 70%, yellow 70-90%, red > 90%)
  - Numerical display (e.g., "1250W / 2000W - 62.5%")
- **HVAC Utilization**:
  - Bar graph showing cooling load vs. capacity
  - Same color coding scheme
  - Heat load calculated from power draw (1W ≈ 3.41 BTU/hr)

### 6. JSON Import/Export
- **Export**: Save current rack configuration as JSON
- **Import**: Load rack configuration from JSON file/paste
- **POST Body Support**: Accept JSON via HTTP POST to auto-populate racks

## Technical Architecture

### Frontend
- **Framework**: Vue 3 (Composition API)
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Drag & Drop**: VueUse (@vueuse/core) useDraggable + useDropZone
- **State Management**: Vue 3 Composition API (ref/reactive) with composables

### Backend
- **Server**: Node.js + Express (minimal)
- **Port**: 3000 (configurable via environment variable)
- **Endpoints**:
  - `GET /` - Serve Vue application
  - `POST /api/load` - Accept JSON rack configuration and redirect/inject
  - Static file serving for built Vue app
- **Default Devices**: JSON file (`src/data/devices.json`)
- **Configuration Storage**:
  - Browser localStorage for automatic persistence
  - Download/upload JSON files for backup/sharing
  - POST endpoint to load configuration programmatically

### Data Models

#### Device Definition
```json
{
  "id": "cisco-c9300-48p",
  "name": "Cisco Catalyst 9300 48-port",
  "category": "network",
  "ruSize": 1,
  "powerDraw": 750,
  "color": "#4A90E2",
  "description": "48-port PoE+ switch"
}
```

#### Rack Configuration
```json
{
  "configId": "datacenter-a-2024",
  "metadata": {
    "createdAt": "2024-01-15T10:30:00Z",
    "lastModified": "2024-01-15T14:22:00Z",
    "description": "Main datacenter rack layout"
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
          "position": 1,
          "instanceId": "switch-core-1",
          "customName": "Core Switch 1"
        },
        {
          "deviceId": "dell-r750",
          "position": 5,
          "instanceId": "esxi-host-1",
          "customName": "ESXi Host 1"
        }
      ]
    }
  ]
}
```

## Implementation Phases

### Phase 1: Core UI & Visualization
- Set up project structure
- Implement rack grid display
- Create device library sidebar with accordions
- Basic styling and responsive layout

### Phase 2: Drag & Drop
- Implement drag and drop functionality
- Device placement logic
- Collision detection
- Visual feedback

### Phase 3: Configuration & Management
- Settings menu for rack/power/HVAC configuration
- Add/remove racks
- Adjust RU per rack

### Phase 4: Resource Tracking
- Calculate total power consumption
- Calculate heat load (BTU/hr)
- Implement utilization bar graphs
- Color-coded warnings

### Phase 5: Data Import/Export
- JSON export functionality
- JSON import via file upload
- JSON import via paste
- POST endpoint (if backend implemented)

### Phase 6: Polish & Features
- Device labeling
- Tooltips with device details
- Search/filter devices
- Undo/redo functionality
- Print/export as image

## Design Decisions & Specifications

### HVAC Calculation
- Use standard formula: **1W power draw = 3.41 BTU/hr heat output**
- HVAC capacity configurable in BTU/hr or watts (auto-convert)
- Heat load = Sum of all device power draw × 3.41

### Drag & Drop Behavior
- **Yes, devices snap to RU boundaries** (can only be placed at RU position 1-42)
- **If insufficient space**: Show visual feedback (red highlight), prevent drop, show tooltip "Not enough space - requires X RU"
- **Between racks**: Yes, devices can be dragged between racks
- **Removal**: Drag device out of rack area OR click X button on device when hovering

### Object Customization
- **Phase 1 (MVP)**: Predefined devices only from devices.json
- **Phase 2 (Future)**: Add ability to create custom devices and edit properties
- **Instance naming**: Users can rename individual device instances in racks (e.g., "Core Switch 1" vs just "Cisco C9300")

### Multi-Rack Layout
- **Default**: Horizontal row (scrollable if many racks)
- **Configurable**: Toggle between horizontal and grid layout
- Each rack labeled with customizable name

### Additional Decisions
- **Technology Stack**: Vue 3 + Tailwind CSS + Node.js/Express
- **Data Persistence**: localStorage + download/upload JSON files
- **JSON POST**: REST API endpoint at `POST /api/load`
- **Device Removal**: Drag out of rack OR hover X button
- **Mobile Support**: Desktop-first, responsive down to tablet (mobile optional)

## File Structure
```
racksum/
├── server.js                 # Express server
├── package.json
├── vite.config.js           # Vite configuration
├── tailwind.config.js       # Tailwind configuration
├── postcss.config.js        # PostCSS configuration
├── .env.example             # Environment variables template
├── .gitignore
├── claude.md                # This file
├── README.md
├── TODO.md
├── index.html               # Vite entry point
├── public/
│   └── favicon.ico
├── src/
│   ├── main.js              # Vue app entry point
│   ├── App.vue              # Root component
│   ├── components/
│   │   ├── DeviceLibrary.vue      # Left sidebar with accordions
│   │   ├── DeviceCategory.vue     # Accordion category component
│   │   ├── DeviceItem.vue         # Draggable device item
│   │   ├── RackContainer.vue      # Main rack display area
│   │   ├── Rack.vue               # Single rack component
│   │   ├── RackSlot.vue           # Individual RU slot
│   │   ├── ConfigMenu.vue         # Settings/configuration modal
│   │   ├── UtilizationPanel.vue   # Power/HVAC bar graphs
│   │   └── ImportExport.vue       # JSON import/export UI
│   ├── composables/
│   │   ├── useRackConfig.js       # Rack state management
│   │   ├── useDevices.js          # Device library management
│   │   ├── useDragDrop.js         # Drag and drop logic
│   │   └── useUtilization.js      # Power/HVAC calculations
│   ├── data/
│   │   └── devices.json           # Default device library
│   ├── utils/
│   │   ├── calculations.js        # Power/HVAC formulas
│   │   └── validators.js          # JSON validation
│   └── assets/
│       └── main.css               # Global styles + Tailwind imports
└── dist/                    # Build output (generated)
```

## Success Criteria
- [ ] Users can visualize 1-N racks with configurable RU heights
- [ ] Device library loads from JSON with categorized accordions
- [ ] Drag and drop devices into racks works smoothly
- [ ] Power and HVAC utilization updates in real-time
- [ ] Visual warnings when capacity exceeded
- [ ] Export rack configuration as JSON
- [ ] Import rack configuration from JSON
- [ ] Works in modern browsers (Chrome, Firefox, Safari, Edge)
- [ ] Responsive design (at minimum for desktop)
