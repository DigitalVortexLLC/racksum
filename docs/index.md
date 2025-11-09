# RackSum

Welcome to RackSum, a comprehensive web-based tool for planning and visualizing server rack layouts with real-time power and HVAC capacity tracking.

## Overview

RackSum simplifies datacenter planning by providing an intuitive drag-and-drop interface for designing rack configurations. It automatically calculates power consumption and heat load, helping you optimize your infrastructure before deployment.

## Key Features

### Interactive Rack Visualization
- **Drag and Drop Interface**: Easily place devices into rack positions
- **Multi-Rack Support**: Configure and manage multiple racks simultaneously
- **Visual Feedback**: Devices automatically snap to RU boundaries for precise placement

### Device Management
- **Comprehensive Device Library**: Pre-configured devices organized by category
  - Power Distribution Units (PDUs)
  - Network Equipment
  - Servers
  - Storage Systems
  - Specialized Equipment
- **Unracked Devices Panel**: Temporary holding area for devices without rack assignments
- **Custom Devices**: Add your own device definitions

### Real-Time Calculations
- **Power Consumption Tracking**: Monitor total power usage across all racks
- **HVAC Heat Load Calculation**: Automatic conversion using industry-standard formula (1W = 3.41 BTU/hr)
- **Refrigeration Tons Display**: HVAC capacity shown in Refrigeration Tons for easy planning
- **Color-Coded Warnings**: Visual indicators for utilization levels
  - Green: < 70% capacity (safe)
  - Yellow: 70-90% capacity (caution)
  - Red: > 90% capacity (critical)

### Data Management
- **Import/Export**: Save and load rack configurations as JSON
- **Persistent Storage**: Automatic saving to browser localStorage
- **REST API**: Programmatically load configurations with POST endpoint

## Tech Stack

- **Frontend**: Vue 3 with Composition API and Vite
- **Styling**: Tailwind CSS with PrimeVue components
- **Backend**: Django REST Framework (with legacy Node.js/Express support)
- **Database**: MySQL with PyMySQL
- **Drag & Drop**: VueUse composables for smooth interactions

## Quick Start

Get started with RackSum in just a few steps:

1. **Install Dependencies**
   ```bash
   npm install
   pip install -r requirements.txt
   ```

2. **Initialize Database**
   ```bash
   npm run db:init
   ```

3. **Start Development Server**
   ```bash
   npm run dev
   ```

4. **Access the Application**

   Navigate to [http://localhost:5173](http://localhost:5173)

## Use Cases

RackSum is perfect for:

- **Datacenter Managers**: Planning new installations or expansions
- **IT Infrastructure Teams**: Visualizing equipment placement
- **Facility Managers**: Ensuring adequate power and cooling
- **Consultants**: Creating client proposals and recommendations
- **Students & Educators**: Learning datacenter design principles

## Getting Help

- Check the [Installation Guide](installation.md) for setup instructions
- Read the [Usage Guide](usage.md) for detailed workflow information
- Review the [API Documentation](api.md) for programmatic access
- Explore [Configuration Options](configuration.md) to customize your setup

## License

RackSum is licensed under the ISC License.
