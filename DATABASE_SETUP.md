# Database Setup Guide

RackSum now supports saving rack configurations to a MySQL database, allowing you to:
- Create and manage multiple sites
- Save rack configurations with names
- Load previously saved configurations
- Share configurations across devices

## Prerequisites

1. MySQL 5.7 or higher installed and running
2. Node.js and npm installed

## Setup Instructions

### 1. Create Database Configuration

Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

### 2. Configure Database Connection

Edit the `.env` file with your MySQL credentials:

```env
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=racksum
```

### 3. Initialize the Database

Run the database initialization script:

```bash
npm run db:init
```

This will:
- Create the `racksum` database
- Create the `sites` table for storing site information
- Create the `rack_configurations` table for storing rack layouts

### 4. Start the Application

```bash
# Development mode
npm run dev

# Production mode
npm start
```

## Database Schema

### Sites Table

Stores information about physical locations/datacenters:

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| name | VARCHAR(255) | Unique site name |
| description | TEXT | Optional description |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

### Rack Configurations Table

Stores complete rack layouts in JSON format:

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| site_id | INT | Foreign key to sites table |
| name | VARCHAR(255) | Configuration name |
| description | TEXT | Optional description |
| config_data | JSON | Complete rack configuration |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

## Usage

### Creating a Site

1. Click the **Save** button in the top menu
2. Click **New Site**
3. Enter a site name (e.g., "DC East", "Production Datacenter")
4. Optionally add a description
5. Click **Create**

### Saving a Rack Configuration

1. Design your rack layout in the application
2. Click the **Save** button in the top menu
3. Select a site (or create a new one)
4. Enter a configuration name (e.g., "Production Rack 1")
5. Optionally add a description
6. Click **Save**

### Loading a Rack Configuration

1. Click the **Load** button in the top menu
2. Select a site from the dropdown
3. Choose a saved configuration from the list
4. Click **Load**

The configuration will be loaded into the application, replacing the current layout.

### Managing Configurations

- **Delete**: Click the trash icon next to a configuration in the load dialog
- **Update**: Save a configuration with the same name to update it
- **Site Management**: Create sites as needed to organize your configurations

## Troubleshooting

### Database Connection Issues

If you see "Database connection unavailable" in the console:

1. Verify MySQL is running:
   ```bash
   # On Linux/Mac
   sudo systemctl status mysql

   # On Windows
   net start MySQL
   ```

2. Check your `.env` file has correct credentials

3. Ensure the MySQL user has proper permissions:
   ```sql
   GRANT ALL PRIVILEGES ON racksum.* TO 'your_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

### Re-initializing the Database

To reset the database (WARNING: This will delete all data):

```sql
DROP DATABASE racksum;
```

Then run:

```bash
npm run db:init
```

## API Endpoints

The server exposes the following REST API endpoints:

### Sites

- `GET /api/sites` - Get all sites
- `GET /api/sites/:id` - Get a specific site
- `POST /api/sites` - Create a new site
- `PUT /api/sites/:id` - Update a site
- `DELETE /api/sites/:id` - Delete a site

### Rack Configurations

- `GET /api/sites/:siteId/racks` - Get all racks for a site
- `GET /api/sites/:siteId/racks/:rackName` - Get a specific rack
- `POST /api/sites/:siteId/racks` - Save a rack configuration
- `DELETE /api/racks/:id` - Delete a rack configuration
- `GET /api/racks` - Get all rack configurations

## Migration from localStorage

Existing configurations stored in browser localStorage will continue to work. You can:

1. Keep using localStorage (no database required)
2. Manually save localStorage configs to the database using the Save feature
3. Use both methods simultaneously

The application will not automatically migrate localStorage data to the database.
