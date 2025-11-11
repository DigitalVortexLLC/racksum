# Resource Providers Guide

This guide explains the new Resource Provider system in RackSum - an additive model for defining site capacity through infrastructure components instead of static values.

## Overview

Previously, RackSum used static configuration values for power and cooling capacity. The new **Resource Provider** system changes this to an **additive model** where you define actual infrastructure components (PDUs, HVAC units, network uplinks, etc.) that contribute capacity to your site.

### Benefits

✅ **More Realistic** - Model your actual infrastructure, not just abstract numbers  
✅ **Easier Planning** - See which specific equipment provides capacity  
✅ **Better Tracking** - Monitor utilization per provider  
✅ **Flexible Growth** - Add providers as your infrastructure expands  
✅ **Redundancy Aware** - Track N+1, 2N, and other redundancy configurations

## Getting Started

### Opening the Resource Providers Manager

1. Click **"Manage Devices"** in the top menu
2. Click the **"Resource Providers"** tab
3. Click **"Add Resource Provider"**

## Provider Types

Resource Providers come in three types:

### 1. Power Providers

Infrastructure that supplies electrical power to your site.

**Examples:**
- PDUs (Power Distribution Units)
- UPS (Uninterruptible Power Supplies)
- Generators
- Utility feeds
- Branch circuits

**Configuration:**
- Name: e.g., "PDU-A01", "UPS-Primary"
- Type: Power
- **Power Capacity**: Maximum watts this provider can supply
- Location: Where the provider is installed
- Description: Additional notes

### 2. Cooling Providers

Infrastructure that provides cooling/HVAC capacity.

**Examples:**
- CRAC units (Computer Room Air Conditioning)
- CRAH units (Computer Room Air Handler)
- Chillers
- Air conditioning units
- Cooling towers

**Configuration:**
- Name: e.g., "CRAC-01", "Chiller-A"
- Type: Cooling
- **Cooling Capacity**: Refrigeration Tons (1 ton = 12,000 BTU/hr)
- Location: Where the provider is installed
- Description: Additional notes

### 3. Network Providers

Infrastructure that provides network connectivity and bandwidth.

**Examples:**
- Core switches
- Distribution switches
- Internet uplinks
- WAN connections
- Fiber links

**Configuration:**
- Name: e.g., "Core-Switch-01", "ISP-Uplink-A"
- Type: Network
- **Network Capacity**: Bandwidth in Gbps
- Location: Where the provider is installed
- Description: Additional notes

## Managing Providers

### Adding a Provider

1. Open Device Manager → Resource Providers tab
2. Click **"Add Resource Provider"**
3. Fill in the required fields:
   - Provider Name
   - Provider Type (Power, Cooling, or Network)
   - Capacity (field changes based on type)
4. Optional: Add location and description
5. Click **"Add Provider"**

### Editing a Provider

1. Find the provider in the list
2. Click the **edit icon** (pencil)
3. Modify any fields
4. Click **"Save Changes"**

### Deleting a Provider

1. Find the provider in the list
2. Click the **delete icon** (trash can)
3. Confirm the deletion

**⚠️ Note:** Deleting a provider reduces your site's total capacity immediately.

## How Capacity is Calculated

RackSum calculates total capacity by **summing all providers** of each type:

```
Total Power Capacity = Sum of all Power Provider capacities
Total Cooling Capacity = Sum of all Cooling Provider capacities
Total Network Capacity = Sum of all Network Provider capacities
```

### Example

If you have:
- PDU-A: 20,000W
- PDU-B: 20,000W
- UPS-01: 30,000W

Your **Total Power Capacity** = 70,000W

## Viewing Resource Providers

### Library Panel

The Device Library panel (left sidebar) has two tabs:
- **Devices Tab**: Browse and drag devices to racks
- **Providers Tab**: Browse and view all resource providers

**In the Providers Tab:**
- Lists all providers grouped by type (Power, Cooling, Network)
- Shows capacity for each provider
- Displays location information
- Provides total capacity summary at the bottom
- Search bar to filter providers by name, location, or description

Click the tabs at the top of the Library panel to switch between Devices and Providers.

### Utilization Details

Click **"View Details"** in the Utilization Panel (bottom-right) to see:

1. **Device Consumption Tab**: Shows what each device consumes
2. **Resource Providers Tab**: Shows provider-by-provider breakdown
   - Capacity per provider
   - Current load distributed across providers
   - Utilization percentage per provider

## Planning Common Scenarios

### Scenario 1: Single Data Center

```
Power Providers:
- Utility Feed A: 100,000W
- Utility Feed B: 100,000W (redundant)
- UPS System: 150,000W

Total Power: 350,000W

Cooling Providers:
- CRAC-01: 10 Tons
- CRAC-02: 10 Tons
- CRAC-03: 10 Tons (redundant N+1)

Total Cooling: 30 Tons
```

### Scenario 2: Edge Location

```
Power Providers:
- Building Power: 10,000W
- UPS: 5,000W

Total Power: 15,000W

Cooling Providers:
- Mini-Split AC: 2.5 Tons

Total Cooling: 2.5 Tons
```

### Scenario 3: Redundant Configuration (2N)

```
Power Providers:
- PDU-A (Circuit 1): 20,000W
- PDU-B (Circuit 2): 20,000W
- Generator Backup: 50,000W

Total Power: 90,000W

Cooling Providers:
- CRAC-A (Primary): 15 Tons
- CRAC-B (Redundant): 15 Tons

Total Cooling: 30 Tons
```

**Note:** RackSum shows total capacity. For 2N redundancy planning, ensure you don't exceed 50% utilization (so you can lose one path).

## Best Practices

### Naming Conventions

Use clear, consistent naming:
- Include equipment type: `PDU-`, `CRAC-`, `UPS-`
- Include location or ID: `A01`, `Row-5`, `Building-2`
- Examples: `PDU-A01`, `CRAC-North-02`, `UPS-Primary`

### Capacity Planning

**Power:**
- Enter the **nameplate rating** or **rated capacity**
- For PDUs: Use the circuit breaker rating (e.g., 30A × 208V = 6,240W)
- For UPS: Use the output capacity in watts
- Account for power factor if needed

**Cooling:**
- Enter the **cooling capacity**, not power consumption
- CRAC/CRAH units usually specify tons or BTU/hr
- 1 Refrigeration Ton = 12,000 BTU/hr = ~3,517 watts of cooling

**Network:**
- Enter the total available bandwidth
- For switches: Port count × speed (e.g., 48 ports × 1Gbps = 48Gbps)
- For uplinks: Actual contracted bandwidth

### Redundancy Planning

RackSum shows **total** capacity. For redundant systems:

**N+1 Strategy:**
- Add all providers (including the +1)
- Plan to use no more than N units worth of capacity
- Example: 3 CRAC units × 10 tons = 30 tons total
- Operate at max 20 tons (2 units) to maintain N+1

**2N Strategy (Dual Path):**
- Add all providers from both paths
- Plan to use no more than 50% capacity
- This ensures either path can handle full load

### Location Tracking

Use the location field to track:
- Physical location: "Row A, Rack 5"
- Building/room: "Building 2, Server Room"
- Logical grouping: "Primary Power Path", "A-Side"

### Documentation

Use the description field for:
- Model numbers: "APC SRT5000"
- Serial numbers
- Maintenance schedules
- Special notes: "Scheduled for upgrade Q2"

## Migration from Static Config

If you're upgrading from the old static configuration:

### Step 1: Note Your Current Settings

Before migrating, note your current capacity values in Configuration.

### Step 2: Add Providers

Add resource providers that match your actual infrastructure.

**Example:**
Old config: 10,000W power capacity
New providers: Add the actual PDUs/UPS units that provide that 10,000W

### Step 3: Verify Totals

Check that your provider totals match or exceed your old static values.

### Step 4: Done!

Once you have providers defined, RackSum automatically uses them. The old static config values become fallback only.

## Import/Export

### Exporting Providers

Resource providers are **not** included in the standard configuration export. They are managed separately like custom devices.

To backup your providers:
1. Go to Device Manager → Import/Export tab
2. Click **Export to JSON**
3. This exports both custom devices and resource providers

### Importing Providers

1. Go to Device Manager → Import/Export tab
2. Choose import mode:
   - **Merge**: Add imported providers without deleting existing ones
   - **Replace**: Delete all existing providers and replace with imported ones
3. Select your JSON file
4. Providers are imported automatically

## Troubleshooting

### Capacity shows 0W or 0 Tons

**Cause:** No resource providers defined  
**Solution:** Add at least one provider of each type you need

### Utilization shows incorrect percentages

**Cause:** Provider capacity is too low or device power draw is incorrectly configured  
**Solution:** 
- Verify provider capacities are correct
- Check device power draw values
- Ensure units are correct (Watts for power, Tons for cooling)

### Can't see my providers

**Cause:** Providers might not be loading  
**Solution:**
- Refresh the page
- Check browser console for errors
- Verify providers are saved (check Device Manager)

### Provider totals don't match my infrastructure

**Cause:** Missing providers or incorrect capacity values  
**Solution:**
- Review all providers in Device Manager
- Compare against your infrastructure documentation
- Update capacities as needed

## Technical Details

### Data Storage

Resource providers are stored in browser localStorage:
- Key: `racksum-resource-providers`
- Format: JSON array of provider objects

### Capacity Calculation

```javascript
totalPowerCapacity = sum(provider.powerCapacity for all power providers)
totalCoolingCapacity = sum(provider.coolingCapacity for all cooling providers)
totalNetworkCapacity = sum(provider.networkCapacity for all network providers)
```

### Fallback Behavior

If no providers are defined, RackSum falls back to the legacy static configuration values. This ensures backward compatibility.

### Event System

When providers change, a `resource-providers-updated` event is dispatched to update all components.

## Example Configurations

### Small Office

```json
{
  "providers": [
    {
      "name": "Building Power",
      "type": "power",
      "powerCapacity": 15000,
      "location": "Server Closet"
    },
    {
      "name": "Portable AC Unit",
      "type": "cooling",
      "coolingCapacity": 18000,
      "location": "Server Closet"
    }
  ]
}
```

### Medium Data Center

```json
{
  "providers": [
    {
      "name": "PDU-A01",
      "type": "power",
      "powerCapacity": 20000,
      "location": "Row A, Hot Aisle"
    },
    {
      "name": "PDU-A02",
      "type": "power",
      "powerCapacity": 20000,
      "location": "Row A, Cold Aisle"
    },
    {
      "name": "CRAC-North",
      "type": "cooling",
      "coolingCapacity": 120000,
      "location": "North Wall"
    },
    {
      "name": "CRAC-South",
      "type": "cooling",
      "coolingCapacity": 120000,
      "location": "South Wall"
    }
  ]
}
```

### Enterprise Data Center

```json
{
  "providers": [
    {
      "name": "Utility-A",
      "type": "power",
      "powerCapacity": 200000,
      "location": "Electrical Room A"
    },
    {
      "name": "Utility-B",
      "type": "power",
      "powerCapacity": 200000,
      "location": "Electrical Room B"
    },
    {
      "name": "Generator-Primary",
      "type": "power",
      "powerCapacity": 500000,
      "location": "Generator Yard"
    },
    {
      "name": "Chiller-01",
      "type": "cooling",
      "coolingCapacity": 360000,
      "location": "Mechanical Room 1"
    },
    {
      "name": "Chiller-02",
      "type": "cooling",
      "coolingCapacity": 360000,
      "location": "Mechanical Room 1"
    },
    {
      "name": "Chiller-03",
      "type": "cooling",
      "coolingCapacity": 360000,
      "location": "Mechanical Room 2"
    }
  ]
}
```

## Need Help?

If you encounter issues or have suggestions for improving the Resource Provider system, please open an issue on the project repository.

---

**Last Updated:** November 8, 2025  
**Feature Version:** 1.0
