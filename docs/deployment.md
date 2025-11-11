# Deployment Guide

This guide covers deploying Racker to production environments.

## Pre-Deployment Checklist

Before deploying to production:

- [ ] Set all environment variables
- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Set `DEBUG=False` in Django settings
- [ ] Configure `ALLOWED_HOSTS` for your domain
- [ ] Set up SSL/TLS certificates
- [ ] Configure database with strong credentials
- [ ] Test the build process locally
- [ ] Set up backup procedures
- [ ] Configure monitoring and logging
- [ ] Review security settings

## Build Process

### Build the Frontend

```bash
# Install dependencies
npm install

# Build for production
npm run build
```

This creates an optimized build in the `dist/` directory with:

- Minified JavaScript and CSS
- Tree-shaken dependencies
- Optimized assets
- Source maps (optional)

### Verify the Build

```bash
# Check build output
ls -lh dist/

# Test the production build locally
npm run preview
```

## Deployment Options

### Option 1: Traditional VPS/Cloud Server

Deploy to a Linux server (Ubuntu, Debian, etc.).

#### 1. Prepare the Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Install Python
sudo apt install -y python3 python3-pip python3-venv

# Install MySQL
sudo apt install -y mysql-server

# Install nginx
sudo apt install -y nginx

# Install PM2 for process management
sudo npm install -g pm2
```

#### 2. Clone and Setup

```bash
# Create application directory
sudo mkdir -p /var/www/racksum
sudo chown $USER:$USER /var/www/racksum

# Clone repository
cd /var/www/racksum
git clone <repository-url> .

# Install dependencies
npm install
pip3 install -r requirements.txt

# Set up environment
cp .env.example .env
nano .env  # Edit configuration
```

#### 3. Configure Database

```bash
# Secure MySQL installation
sudo mysql_secure_installation

# Create database and user
sudo mysql -u root -p
```

```sql
CREATE DATABASE racksum CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'racksum_user'@'localhost' IDENTIFIED BY 'secure_password_here';
GRANT ALL PRIVILEGES ON racksum.* TO 'racksum_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

```bash
# Run migrations
cd backend
python3 manage.py migrate
python3 manage.py collectstatic --no-input
cd ..
```

#### 4. Build Application

```bash
# Build frontend
npm run build
```

#### 5. Configure nginx

Create `/etc/nginx/sites-available/racksum`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Static files
    location /static/ {
        alias /var/www/racksum/backend/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # API requests
    location /api/ {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Frontend application
    location / {
        root /var/www/racksum/dist;
        try_files $uri $uri/ /index.html;
        expires 1h;
        add_header Cache-Control "public";
    }

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript
               application/x-javascript application/xml+rss
               application/json application/javascript;
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/racksum /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 6. SSL Certificate with Let's Encrypt

```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is configured automatically
# Test renewal
sudo certbot renew --dry-run
```

#### 7. Start Application with PM2

```bash
# Start Django backend
cd /var/www/racksum/backend
pm2 start "python3 manage.py runserver 3000" --name racksum-backend

# Save PM2 configuration
pm2 save

# Set PM2 to start on boot
pm2 startup systemd
# Follow the instructions provided by the command
```

#### 8. Configure Firewall

```bash
# Allow SSH, HTTP, and HTTPS
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```

### Option 2: Docker Deployment

Use Docker for containerized deployment.

#### Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
# Multi-stage build

# Stage 1: Build frontend
FROM node:20 AS frontend-builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Python backend
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend ./backend
COPY --from=frontend-builder /app/dist ./dist

# Collect static files
WORKDIR /app/backend
RUN python manage.py collectstatic --no-input

# Expose port
EXPOSE 3000

# Start application
CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]
```

#### Create docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MYSQL_DATABASE: ${DB_NAME}
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - racksum-network

  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DB_HOST=db
      - DB_PORT=3306
      - DB_NAME=${DB_NAME}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=False
    depends_on:
      - db
    volumes:
      - ./backend:/app/backend
      - static_files:/app/backend/staticfiles
    networks:
      - racksum-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./dist:/usr/share/nginx/html
      - static_files:/usr/share/nginx/html/static
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    networks:
      - racksum-network

volumes:
  mysql_data:
  static_files:

networks:
  racksum-network:
    driver: bridge
```

#### Deploy with Docker

```bash
# Create .env file
cp .env.example .env
nano .env  # Edit configuration

# Build and start containers
docker-compose up -d

# Run migrations
docker-compose exec app python backend/manage.py migrate

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

### Option 3: Cloud Platform (Heroku)

Deploy to Heroku for quick cloud deployment.

#### 1. Prepare for Heroku

Create `Procfile`:

```
web: cd backend && gunicorn backend.wsgi --bind 0.0.0.0:$PORT
```

Create `runtime.txt`:

```
python-3.11.0
```

Update `requirements.txt`:

```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

#### 2. Deploy to Heroku

```bash
# Install Heroku CLI
# (See https://devcenter.heroku.com/articles/heroku-cli)

# Login
heroku login

# Create app
heroku create your-app-name

# Add MySQL addon
heroku addons:create cleardb:ignite

# Set environment variables
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set DEBUG=False

# Deploy
git push heroku main

# Run migrations
heroku run python backend/manage.py migrate

# Open app
heroku open
```

### Option 4: Serverless (Vercel/Netlify)

Deploy frontend to Vercel/Netlify, backend to serverless functions.

#### Frontend to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd /path/to/racksum
vercel --prod
```

Create `vercel.json`:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "rewrites": [
    { "source": "/api/(.*)", "destination": "https://your-backend-api.com/api/$1" },
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

## Post-Deployment

### Verify Deployment

```bash
# Test endpoints
curl https://yourdomain.com
curl https://yourdomain.com/api/devices

# Check SSL
curl -I https://yourdomain.com

# Monitor logs
pm2 logs racksum-backend
# or
docker-compose logs -f
```

### Set Up Monitoring

#### PM2 Monitoring

```bash
# Monitor with PM2
pm2 monit

# Generate startup script
pm2 startup
pm2 save
```

#### Application Monitoring

Use services like:

- **Sentry** for error tracking
- **New Relic** for performance monitoring
- **Datadog** for infrastructure monitoring
- **Uptime Robot** for uptime monitoring

### Configure Backups

#### Database Backups

```bash
# Create backup script
sudo nano /usr/local/bin/backup-racksum.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/racksum"
mkdir -p $BACKUP_DIR

# Backup database
mysqldump -u racksum_user -p'password' racksum | gzip > "$BACKUP_DIR/db_$DATE.sql.gz"

# Backup device library
cp /var/www/racksum/src/data/devices.json "$BACKUP_DIR/devices_$DATE.json"

# Remove backups older than 30 days
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.json" -mtime +30 -delete
```

```bash
# Make executable
sudo chmod +x /usr/local/bin/backup-racksum.sh

# Schedule with cron (daily at 2 AM)
sudo crontab -e
```

Add:

```
0 2 * * * /usr/local/bin/backup-racksum.sh
```

### Set Up Log Rotation

```bash
# Create logrotate configuration
sudo nano /etc/logrotate.d/racksum
```

```
/var/www/racksum/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        pm2 reloadLogs
    endscript
}
```

## Performance Optimization

### Enable Caching

Configure nginx caching:

```nginx
# Add to nginx config
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=100m inactive=60m;

location /api/devices {
    proxy_cache api_cache;
    proxy_cache_valid 200 1h;
    proxy_cache_key "$request_uri";
    add_header X-Cache-Status $upstream_cache_status;
    proxy_pass http://localhost:3000;
}
```

### CDN Integration

Use a CDN for static assets:

1. Upload `dist/` to CDN (e.g., CloudFlare, AWS CloudFront)
2. Update base URL in application
3. Configure cache headers

### Database Optimization

```sql
-- Add indexes
CREATE INDEX idx_rack_id ON devices(rack_id);
CREATE INDEX idx_category ON devices(category);

-- Optimize tables
OPTIMIZE TABLE devices;
OPTIMIZE TABLE racks;
```

## Security Hardening

### Application Security

1. **Rate Limiting**

```python
# Install django-ratelimit
pip install django-ratelimit

# Add to views
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='100/h')
def load_configuration(request):
    # ...
```

2. **CSRF Protection**

```python
# Ensure CSRF middleware is enabled
MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
    # ...
]
```

3. **Security Headers**

```python
# Add to settings.py
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Server Security

```bash
# Disable root login
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no

# Configure fail2ban
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Keep system updated
sudo apt update && sudo apt upgrade -y
```

## Troubleshooting

### Application Won't Start

```bash
# Check PM2 logs
pm2 logs racksum-backend

# Check nginx logs
sudo tail -f /var/log/nginx/error.log

# Check system logs
sudo journalctl -u nginx -f
```

### Database Connection Issues

```bash
# Test MySQL connection
mysql -u racksum_user -p -h localhost racksum

# Check MySQL service
sudo systemctl status mysql

# Review MySQL logs
sudo tail -f /var/log/mysql/error.log
```

### SSL Certificate Issues

```bash
# Test SSL
openssl s_client -connect yourdomain.com:443

# Renew certificate
sudo certbot renew

# Check certificate expiry
sudo certbot certificates
```

## Maintenance

### Update Application

```bash
# Pull latest code
cd /var/www/racksum
git pull origin main

# Install dependencies
npm install
pip install -r requirements.txt

# Build frontend
npm run build

# Run migrations
cd backend
python3 manage.py migrate
python3 manage.py collectstatic --no-input

# Restart application
pm2 restart racksum-backend

# Reload nginx
sudo systemctl reload nginx
```

### Monitor Resources

```bash
# Check disk usage
df -h

# Check memory usage
free -h

# Check CPU usage
top

# Check PM2 status
pm2 status

# Check logs size
du -sh /var/log
```

## Scaling

### Horizontal Scaling

Deploy multiple application servers behind a load balancer:

```nginx
upstream racksum_backends {
    server 192.168.1.10:3000;
    server 192.168.1.11:3000;
    server 192.168.1.12:3000;
}

server {
    location /api/ {
        proxy_pass http://racksum_backends;
    }
}
```

### Database Scaling

- Set up MySQL replication
- Use read replicas for queries
- Implement connection pooling

### Caching Layer

Add Redis for session/data caching:

```bash
# Install Redis
sudo apt install redis-server

# Configure Django to use Redis
pip install django-redis
```

## Next Steps

- Set up monitoring dashboards
- Configure automated backups
- Implement CI/CD pipeline
- Review [Configuration Guide](configuration.md)
