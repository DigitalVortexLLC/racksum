# Usage Guide

This guide provides detailed instructions on how to use RackSum for rack planning and management.

## Getting Started

### First Launch

When you first launch RackSum, you'll see:

1. An empty rack visualization area in the center
2. A device library panel on the left
3. An unracked devices panel on the right
4. A utilization panel in the bottom-right corner
5. Action buttons in the top toolbar

## Basic Workflow

### Step 1: Configure Your Environment

Before adding devices, set up your infrastructure parameters:

1. Click the **Configure** button in the toolbar
2. In the configuration dialog, enter:
   - **Number of Racks**: How many racks you want to manage (default: 2)
   - **RU per Rack**: Rack units per rack (default: 42)
   - **Total Power Capacity**: Available power in Watts (default: 10000W)
   - **HVAC Capacity**: Cooling capacity in Refrigeration Tons (default: 10 tons)
3. Click **Save** to apply changes

**Example Configuration:**

```
Racks: 4
RU per Rack: 42
Power Capacity: 20000W
HVAC Capacity: 20 Refrigeration Tons
```

### Step 2: Understanding the Device Library

The left sidebar contains pre-configured devices organized by category:

#### Device Categories

1. **Power Distribution**
   - APC Smart-UPS models
   - Eaton 5P series
   - Various wattage capacities

2. **Network Equipment**
   - Cisco Catalyst switches
   - Nexus series switches
   - Routers and firewalls

3. **Servers**
   - Dell PowerEdge series
   - HP ProLiant servers
   - Various form factors (1U, 2U, 4U)

4. **Storage Systems**
   - NetApp FAS systems
   - Dell EMC Unity
   - HPE 3PAR

5. **Specialized Equipment**
   - Blade chassis
   - Custom appliances
   - Other datacenter equipment

#### Device Information

Each device card shows:
- Device name
- RU size (rack units)
- Power draw in Watts
- Color-coded category indicator

### Step 3: Adding Devices to Racks

#### Drag and Drop Method

1. Locate a device in the library
2. Click and hold the device card
3. Drag the device over to the desired rack
4. Position it at the desired RU location
5. Release to drop the device

**Tips:**
- Devices automatically snap to RU boundaries
- You cannot place a device where there isn't enough space
- Devices cannot overlap with existing devices
- The cursor shows a preview while dragging

#### Keyboard Navigation

For precise placement:

1. Tab through devices in the library
2. Press Enter to select a device
3. Use arrow keys to navigate rack positions
4. Press Enter to place the device

### Step 4: Managing Devices in Racks

#### Viewing Device Details

Click on any placed device to see:
- Full device specifications
- Power consumption
- Heat load (BTU/hr)
- Current position and rack assignment

#### Moving Devices

To reposition a device within or between racks:

1. Click and drag the device from its current position
2. Move it to the new location
3. Release to drop

#### Removing Devices

To remove a device from a rack:

1. Right-click on the device
2. Select **Remove** from the context menu
3. The device moves to the Unracked Devices panel

Or:
1. Drag the device to the Unracked Devices panel
2. Release to move it there

#### Customizing Device Names

To give a device instance a custom name:

1. Click on the device
2. In the detail modal, find the **Custom Name** field
3. Enter your desired name (e.g., "Production DB Server")
4. Click **Save**

### Step 5: Working with Unracked Devices

The Unracked Devices panel on the right shows:
- Devices without rack assignments
- Devices imported via API without position data
- Devices you've removed from racks

#### Adding Unracked Devices to Racks

1. Find the device in the Unracked Devices panel
2. Drag it to a rack at the desired position
3. Release to place it

#### Viewing Unracked Device Stats

The utilization panel includes power consumption from unracked devices, helping you plan capacity before placement.

### Step 6: Monitoring Resource Utilization

The bottom-right panel shows real-time statistics:

#### Power Usage

```
Power: 4,250W / 10,000W (42.5%)
```

- Shows total power consumption vs. capacity
- Includes both racked and unracked devices
- Color-coded: Green (safe), Yellow (caution), Red (critical)

#### HVAC Load

```
HVAC: 6.8 Tons / 10.0 Tons (68.0%)
```

- Heat load calculated from power consumption
- Displayed in Refrigeration Tons
- Formula: Tons = (Power in Watts × 3.41) / 12000
- Color-coded capacity warnings

#### Utilization Indicators

| Color | Range | Meaning |
|-------|-------|---------|
| Green | < 70% | Safe operating range |
| Yellow | 70-90% | Approaching capacity |
| Red | > 90% | Critical - add capacity |

#### Detailed Resource View

Click on the utilization panel to see:
- Per-rack power consumption
- Per-rack heat load
- Device-by-device breakdown
- Capacity recommendations

## Advanced Features

### Import/Export Configurations

#### Exporting a Configuration

1. Click the **Import/Export** button
2. Choose your export format:
   - **Copy JSON**: Copy to clipboard
   - **Download File**: Save as `.json` file
3. The export includes:
   - All rack configurations
   - All devices (racked and unracked)
   - Settings and metadata

#### Importing a Configuration

1. Click the **Import/Export** button
2. Choose your import method:
   - **Paste JSON**: Paste from clipboard
   - **Upload File**: Select a `.json` file
3. Click **Import**
4. The configuration loads and replaces the current setup

**Warning:** Importing overwrites your current configuration. Export first if you want to save it.

### Using the REST API

Load configurations programmatically using the API endpoint.

#### Basic POST Request

```bash
curl -X POST http://localhost:3000/api/load \
  -H "Content-Type: application/json" \
  -d @rack-config.json
```

#### API Response

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

#### Automatic Unracked Device Handling

When POSTing configurations, devices are handled three ways:

1. **In Racks**: Devices with `position` and `rackId` go directly into racks
2. **Explicitly Unracked**: Devices in `unrackedDevices` array go to the panel
3. **Auto-Unracked**: Devices in `devices` array without position data automatically go to Unracked Devices

This allows you to import device lists where positions haven't been determined yet.

### Saving to Browser Storage

RackSum automatically saves your configuration to localStorage:

- Saves occur on every change
- Data persists across browser sessions
- Cleared only when you clear browser data

To manually clear:

1. Open browser DevTools (F12)
2. Go to Application > Local Storage
3. Find and delete `racksum-config`

### Dark Mode

Toggle dark mode for comfortable viewing:

1. Click the theme toggle button (moon/sun icon)
2. Dark mode preference is saved
3. Applies across all sessions

## Common Workflows

### Scenario 1: Planning a New Datacenter

1. Configure total racks, power, and HVAC capacity
2. Add devices to Unracked Devices panel
3. Calculate total power and heat requirements
4. Arrange devices in racks for optimal layout
5. Monitor utilization to ensure capacity
6. Export configuration for reference

### Scenario 2: Expanding Existing Infrastructure

1. Import current rack configuration
2. Add new racks via Configure menu
3. Add new devices from library
4. Place new devices in empty spaces
5. Verify power and HVAC capacity
6. Export updated configuration

### Scenario 3: Capacity Planning

1. Load current configuration
2. Add planned devices to Unracked panel
3. Check utilization percentages
4. Determine if capacity upgrades needed
5. Try different arrangements
6. Export final plan

### Scenario 4: API Integration

1. Generate device inventory in external system
2. Format as RackSum JSON
3. POST to `/api/load` endpoint
4. Review in RackSum UI
5. Assign positions via drag-and-drop
6. Export finalized configuration

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl/Cmd + S` | Quick save (export config) |
| `Ctrl/Cmd + O` | Open import dialog |
| `Ctrl/Cmd + E` | Toggle export dialog |
| `Escape` | Close any open modal |
| `Tab` | Navigate through devices |
| `Enter` | Select/place device |
| `Delete` | Remove selected device |

## Best Practices

### Power Planning

- Leave 20-30% power capacity headroom
- Account for future growth
- Consider redundancy requirements
- Monitor individual rack loads

### Cooling Planning

- Ensure HVAC capacity exceeds heat load
- Consider hot aisle/cold aisle arrangements
- Account for ambient temperature
- Plan for equipment redundancy

### Device Organization

- Group similar devices together
- Place heavy power users strategically
- Consider cable management
- Document custom names and purposes

### Data Management

- Export configurations regularly
- Use descriptive file names
- Version your configurations
- Keep backups of critical layouts

## Troubleshooting

### Devices Won't Place

**Problem:** Cannot drop device into rack

**Solutions:**
- Check if there's enough vertical space (RU)
- Verify no overlapping devices
- Ensure position is within rack boundaries
- Try zooming in for more precise placement

### Utilization Not Updating

**Problem:** Stats panel shows outdated information

**Solutions:**
- Refresh the page
- Check browser console for errors
- Clear localStorage and reimport config
- Verify all devices have power draw values

### Import Fails

**Problem:** Configuration JSON won't import

**Solutions:**
- Validate JSON syntax
- Check required fields are present
- Ensure device IDs match library
- Review error message in console

### Lost Configuration

**Problem:** Configuration disappeared after reload

**Solutions:**
- Check browser localStorage wasn't cleared
- Look for autosave backup
- Check if import overwrote it
- Use previous export if available

## Next Steps

- Learn about [Configuration Options](configuration.md)
- Explore the [API Documentation](api.md)
- Review [Deployment Guide](deployment.md)
- Read about [Custom Devices](configuration.md#custom-devices)
