# Custom Devices Guide

This guide explains how to create, manage, and share custom device groups and devices in RackSum.

## Overview

RackSum now allows you to define your own device groups and devices through the Device Manager interface. This is perfect for:

- Adding equipment not in the default library
- Creating custom configurations for specific hardware
- Organizing devices by your own categorization scheme
- Sharing device libraries with your team

## Getting Started

### Opening the Device Manager

Click the **"Manage Devices"** button in the configuration menu to open the Device Manager.

The Device Manager has three tabs:
1. **Device Groups** - Create and manage device categories
2. **Devices** - Create and manage individual devices
3. **Import/Export** - Share and backup your custom devices

## Managing Device Groups

Device groups are categories that organize your devices (e.g., "Servers", "Storage", "Network Equipment").

### Creating a New Group

1. Click the **Device Groups** tab
2. Click **Add Device Group**
3. Enter a descriptive name (e.g., "My Servers", "Network Switches")
4. Choose a default color for devices in this group
5. Click **Add Group**

### Editing a Group

1. Find the group in the list
2. Click the **edit icon** (pencil)
3. Modify the name or color
4. Click **Save Changes**

**Note:** If you change a group's name, all devices in that group will be automatically updated.

### Deleting a Group

1. Find the group in the list
2. Click the **delete icon** (trash can)
3. Confirm the deletion

**Note:** Deleting a group does NOT delete the devices in that group.

## Managing Devices

### Creating a New Device

1. Click the **Devices** tab
2. Click **Add Device**
3. Fill in the required fields:
   - **Device Model Name** (e.g., "Dell PowerEdge R750")
   - **Device Group** - Select from your groups
   - **RU Size** - Height in rack units (1-42)
   - **Power Draw** - Maximum power consumption in watts
4. Optional fields:
   - **Color** - Override the group's default color
   - **Description** - Additional details
5. Click **Add Device**

### Editing a Device

1. Find the device in the list
2. Click the **edit icon** (pencil)
3. Modify any fields
4. Click **Save Changes**

### Duplicating a Device

Need to create a variant of an existing device? Use the duplicate feature:

1. Find the device in the list
2. Click the **duplicate icon** (two squares)
3. Modify the fields (the name will have "(Copy)" appended)
4. Click **Create Duplicate**

This is perfect for creating multiple configurations of the same hardware model.

### Deleting a Device

1. Find the device in the list
2. Click the **delete icon** (trash can)
3. Confirm the deletion

## Import/Export

Share your custom devices with team members or backup your library.

### Exporting Devices

1. Click the **Import/Export** tab
2. Click **Export to JSON**
3. A JSON file will be downloaded with all your custom groups and devices

The filename will be: `racksum-devices-YYYY-MM-DD.json`

### Importing Devices

1. Click the **Import/Export** tab
2. Choose an import mode:
   - **Merge** - Add new devices without deleting existing ones
   - **Replace** - Delete all existing custom devices and replace with imported ones
3. Click **Select JSON File**
4. Choose your JSON file
5. The devices will be imported automatically

### JSON File Format

The export/import file follows this structure:

```json
{
  "groups": [
    {
      "id": "group-1234567890",
      "name": "My Servers",
      "color": "#9B59B6",
      "deviceCount": 2
    }
  ],
  "devices": [
    {
      "id": "device-1234567890",
      "name": "Custom Server Model",
      "category": "My Servers",
      "ruSize": 2,
      "powerDraw": 850,
      "color": "#9B59B6",
      "description": "Custom server configuration",
      "custom": true
    }
  ],
  "exportDate": "2025-11-08T12:00:00.000Z",
  "version": "1.0"
}
```

## Using Custom Devices

Once created, your custom devices appear in the Device Library alongside the default devices.

**Visual Indicators:**
- Custom devices display a blue **"Custom"** badge
- Custom devices can be dragged into racks just like default devices
- Custom devices are automatically saved with your rack configurations

## Tips and Best Practices

### Naming Conventions

- **Groups**: Use clear, broad categories (e.g., "Enterprise Servers", "Edge Switches")
- **Devices**: Include manufacturer and model (e.g., "Dell PowerEdge R750", "Cisco 9300-48P")

### Power Draw

Always enter the **maximum** power draw under full load. This ensures accurate power capacity planning.

### RU Size

- 1U = 1.75 inches (44.45mm)
- Most rack-mount servers are 1U, 2U, or 4U
- Some PDUs are 0U (zero-U) as they don't occupy rack space

### Colors

- Stick with your group's default color for consistency
- Use custom colors only when you need to highlight specific devices
- Use color-blind friendly palettes for better accessibility

### Descriptions

Include helpful information in the description:
- CPU/RAM specifications
- Network port types and counts
- Storage capacity
- Special features or requirements

### Backup and Sharing

- **Export regularly** to backup your custom devices
- Share device libraries across your organization for consistency
- Version your exports (e.g., `racksum-devices-datacenter-a-v2.json`)

## Data Storage

Custom devices are stored in your browser's local storage:
- `racksum-device-groups` - Your custom groups
- `racksum-custom-devices` - Your custom devices

This means:
- ✅ Your data persists between sessions
- ✅ No server upload required
- ⚠️ Data is browser-specific (use export/import to move between browsers)
- ⚠️ Clearing browser data will delete custom devices (use export for backup)

## Troubleshooting

### My custom devices aren't showing up

1. Check that you've selected the correct device group when filtering
2. Try refreshing the page
3. Verify the devices exist in the Devices tab of Device Manager

### Import failed

Common issues:
- **Invalid JSON**: Ensure the file is valid JSON format
- **Missing fields**: All required fields (name, category, ruSize, powerDraw) must be present
- **Corrupted file**: Try exporting and importing again

### Devices disappeared

If you cleared your browser data, your custom devices were deleted. Always keep an exported backup!

## Need Help?

If you encounter issues or have suggestions for improving custom device management, please open an issue on the project repository.

---

**Last Updated:** November 8, 2025  
**Feature Version:** 1.0
