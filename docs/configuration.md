# Configuration Guide

This guide explains how to configure and customize RackSum for your specific needs.

## Environment Configuration

### Environment Variables

RackSum uses environment variables for configuration. Create a `.env` file in the project root:

```env
# Server Configuration
PORT=3000
NODE_ENV=production

# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=racksum
DB_USER=racksum_user
DB_PASSWORD=your_secure_password

# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:5173,https://yourdomain.com
```

### Environment Variable Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `PORT` | Server port | `3000` | No |
| `NODE_ENV` | Environment mode | `development` | No |
| `DB_HOST` | Database host | `localhost` | Yes* |
| `DB_PORT` | Database port | `3306` | Yes* |
| `DB_NAME` | Database name | `racksum` | Yes* |
| `DB_USER` | Database username | - | Yes* |
| `DB_PASSWORD` | Database password | - | Yes* |
| `SECRET_KEY` | Django secret key | - | Yes |
| `DEBUG` | Debug mode | `True` | No |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost` | No |

*Required only if using database features

## Application Settings

### Default Rack Configuration

Edit the default settings in the configuration modal or set them via API:

```json
{
  "settings": {
    "totalPowerCapacity": 10000,
    "hvacCapacity": 10,
    "ruPerRack": 42
  }
}
```

#### Power Capacity

Total available power in Watts.

**Common Values:**
- Small lab: 5,000 - 10,000W
- Medium datacenter: 20,000 - 50,000W
- Large datacenter: 100,000+ W

**Calculation:**
```
Power Capacity (W) = Circuit Amperage × Voltage × Number of Circuits

Example:
2 circuits × 20A × 120V = 4,800W
```

#### HVAC Capacity

Cooling capacity in Refrigeration Tons.

**Conversion:**
- 1 Refrigeration Ton = 12,000 BTU/hr
- 1 Watt = 3.41 BTU/hr

**Formula:**
```
HVAC Capacity (Tons) = (Power Capacity in Watts × 3.41) / 12,000

Example:
(10,000W × 3.41) / 12,000 = 2.84 Tons
```

**Common Values:**
- Small server room: 2-5 Tons
- Medium datacenter: 10-30 Tons
- Large datacenter: 50+ Tons

#### RU per Rack

Standard rack heights:

| Type | RU | Height |
|------|----|---------
| Half rack | 21 | ~1m |
| Full rack | 42 | ~2m |
| Tall rack | 45-48 | ~2.2m |

Most datacenters use **42U** racks as the standard.

## Custom Devices

### Adding Custom Devices

Edit `src/data/devices.json` to add your own device definitions.

#### Device JSON Structure

```json
{
  "categories": [
    {
      "id": "custom",
      "name": "Custom Equipment",
      "devices": [
        {
          "id": "my-device-id",
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

#### Device Properties

| Property | Type | Description | Required |
|----------|------|-------------|----------|
| `id` | string | Unique identifier | Yes |
| `name` | string | Display name | Yes |
| `category` | string | Category ID | Yes |
| `ruSize` | number | Rack units (1, 2, 4, etc.) | Yes |
| `powerDraw` | number | Power consumption in Watts | Yes |
| `color` | string | Hex color code | Yes |
| `description` | string | Device description | No |

#### Categories

Valid category values:

- `power` - Power distribution units
- `network` - Switches, routers, firewalls
- `servers` - Rack servers
- `storage` - Storage arrays
- `specialized` - Specialized equipment
- `custom` - Custom devices

#### Example: Adding a GPU Server

```json
{
  "id": "custom",
  "name": "Custom Equipment",
  "devices": [
    {
      "id": "nvidia-dgx-a100",
      "name": "NVIDIA DGX A100",
      "category": "servers",
      "ruSize": 6,
      "powerDraw": 6500,
      "color": "#76B900",
      "description": "8x A100 GPU server for AI/ML workloads"
    }
  ]
}
```

#### Example: Adding Network Equipment

```json
{
  "id": "juniper-qfx5200",
  "name": "Juniper QFX5200",
  "category": "network",
  "ruSize": 1,
  "powerDraw": 450,
  "color": "#3498DB",
  "description": "32-port 100GbE switch"
}
```

#### Color Coding Best Practices

Use consistent colors for device categories:

```
Power:       #E74C3C (Red)
Network:     #3498DB (Blue)
Servers:     #8E44AD (Purple)
Storage:     #E67E22 (Orange)
Specialized: #1ABC9C (Teal)
Custom:      #95A5A6 (Gray)
```

### Device Library Management

#### Backup Device Library

Before making changes:

```bash
cp src/data/devices.json src/data/devices.json.backup
```

#### Validate JSON

Use a JSON validator to ensure syntax correctness:

```bash
# Using jq
cat src/data/devices.json | jq '.'

# Using Python
python -m json.tool src/data/devices.json
```

#### Reload Changes

After editing the device library:

1. Save the file
2. Refresh the browser (Ctrl/Cmd + R)
3. Devices appear in the library immediately

## Database Configuration

### MySQL Setup

#### Create Database

```sql
CREATE DATABASE racksum CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### Create User

```sql
CREATE USER 'racksum_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON racksum.* TO 'racksum_user'@'localhost';
FLUSH PRIVILEGES;
```

#### Configure Connection

Update `.env` with database credentials:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=racksum
DB_USER=racksum_user
DB_PASSWORD=your_secure_password
```

#### Run Migrations

```bash
cd backend
python manage.py migrate
```

### Database Schema

The database stores:

- Saved configurations
- User preferences
- Audit logs
- Custom device definitions

See `src/db/schema.sql` for the complete schema.

## Frontend Configuration

### Vite Configuration

Edit `vite.config.js` for build and dev server settings:

```javascript
export default {
  server: {
    port: 5173,
    host: true,  // Expose to network
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true
  }
}
```

### Tailwind Configuration

Customize styling in `tailwind.config.js`:

```javascript
export default {
  theme: {
    extend: {
      colors: {
        primary: '#3498DB',
        secondary: '#8E44AD',
        success: '#27AE60',
        warning: '#F39C12',
        danger: '#E74C3C'
      }
    }
  }
}
```

### PrimeVue Theme

Configure PrimeVue theme in `src/main.js`:

```javascript
import PrimeVue from 'primevue/config';
import 'primevue/resources/themes/lara-light-blue/theme.css';

app.use(PrimeVue, {
  ripple: true,
  inputStyle: 'filled'
});
```

## Backend Configuration

### Django Settings

Edit `backend/backend/settings.py`:

#### CORS Configuration

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://yourdomain.com",
]

CORS_ALLOW_CREDENTIALS = True
```

#### Database Configuration

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'racksum'),
        'USER': os.getenv('DB_USER', 'racksum_user'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}
```

#### Static Files

```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

### API Configuration

Configure API endpoints in `backend/api/urls.py`:

```python
urlpatterns = [
    path('devices/', views.get_devices, name='get_devices'),
    path('load/', views.load_configuration, name='load_configuration'),
    path('save/', views.save_configuration, name='save_configuration'),
]
```

## Performance Tuning

### Browser Storage Limits

LocalStorage has a 5-10MB limit per domain. For large configurations:

1. Use IndexedDB instead
2. Implement server-side storage
3. Compress JSON data

### Rendering Performance

For many racks/devices:

1. Enable virtual scrolling
2. Lazy load device cards
3. Throttle drag events
4. Use CSS transforms for animations

### API Performance

Optimize API calls:

1. Implement response caching
2. Use HTTP compression (gzip)
3. Minimize payload sizes
4. Use CDN for static assets

## Security Configuration

### Production Security Checklist

- [ ] Change default `SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable HTTPS
- [ ] Implement CSRF protection
- [ ] Add authentication to API
- [ ] Set up rate limiting
- [ ] Use environment variables for secrets
- [ ] Enable database encryption
- [ ] Configure firewall rules

### HTTPS Configuration

Use a reverse proxy (nginx) for HTTPS:

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### API Security

Add authentication middleware:

```python
# backend/api/middleware.py
class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        api_key = request.headers.get('X-API-Key')
        if not self.validate_key(api_key):
            return JsonResponse({'error': 'Invalid API key'}, status=401)
        return self.get_response(request)
```

## Monitoring and Logging

### Application Logs

Configure logging in Django:

```python
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'racksum.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```

### Access Logs

Track API usage:

```python
# Log all API requests
def log_api_request(request):
    logger.info(f"{request.method} {request.path} - {request.META.get('REMOTE_ADDR')}")
```

### Error Monitoring

Integrate error tracking (e.g., Sentry):

```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

## Backup and Recovery

### Configuration Backup

Automated backup script:

```bash
#!/bin/bash
# backup-configs.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/racksum"

# Backup device library
cp src/data/devices.json "$BACKUP_DIR/devices_$DATE.json"

# Backup database
mysqldump -u racksum_user -p racksum > "$BACKUP_DIR/db_$DATE.sql"

# Keep only last 30 days
find "$BACKUP_DIR" -name "*.json" -mtime +30 -delete
find "$BACKUP_DIR" -name "*.sql" -mtime +30 -delete
```

### Restore Procedure

```bash
# Restore device library
cp /backups/racksum/devices_20240115_120000.json src/data/devices.json

# Restore database
mysql -u racksum_user -p racksum < /backups/racksum/db_20240115_120000.sql
```

## Next Steps

- Review [Deployment Guide](deployment.md) for production setup
- Explore [Development Guide](development.md) for customization
- Check [API Reference](api.md) for integration options
