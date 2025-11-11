# Installation Guide

This guide will walk you through installing and setting up Racker on your system.

## Prerequisites

Before installing Racker, ensure you have the following software installed:

### Required Software

- **Node.js**: Version 20 or higher
  - Download from [nodejs.org](https://nodejs.org/)
  - Verify installation: `node --version`

- **Python**: Version 3.8 or higher
  - Download from [python.org](https://www.python.org/)
  - Verify installation: `python --version`

- **npm**: Comes bundled with Node.js
  - Verify installation: `npm --version`

- **MySQL**: Version 5.7 or higher (optional for database features)
  - Download from [mysql.com](https://www.mysql.com/)
  - Verify installation: `mysql --version`

### System Requirements

- **Operating System**: Linux, macOS, or Windows
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: 500MB for application and dependencies
- **Browser**: Modern browser (Chrome, Firefox, Safari, or Edge)

## Installation Steps

### 1. Clone the Repository

```bash
# Clone the repository
git clone https://github.com/DigitalVortexLLC/racker.git
cd racker
```

If you downloaded a ZIP file instead:

```bash
# Extract and navigate to the directory
unzip racker.zip
cd racker
```

### 2. Install Node.js Dependencies

```bash
npm install
```

This will install all required frontend dependencies including:

- Vue 3
- Vite
- Tailwind CSS
- PrimeVue
- VueUse
- And other dependencies listed in `package.json`

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or if you prefer using pip3:

```bash
pip3 install -r requirements.txt
```

This installs:

- Django 5.2.8
- Django REST Framework
- Django CORS Headers
- PyMySQL
- python-dotenv
- MkDocs (for documentation)
- MkDocs Material theme

### 4. Configure Environment Variables (Optional)

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` to configure:

```env
# Server Configuration
PORT=3000

# Database Configuration (if using MySQL)
DB_HOST=localhost
DB_PORT=3306
DB_NAME=racker
DB_USER=your_username
DB_PASSWORD=your_password

# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True

# Authentication (optional - set to 1 to require authentication)
REQUIRE_AUTH=0
```

### 5. Initialize Database (Optional)

If you want to use database features:

```bash
# Run Django migrations
npm run db:init
```

Or manually:

```bash
cd backend
python manage.py migrate
cd ..
```

### 6. Verify Installation

Check that everything is installed correctly:

```bash
# Check Node.js dependencies
npm list --depth=0

# Check Python dependencies
pip list
```

## Running the Application

### Development Mode

Racker uses a dual-server architecture for development:
- **Vite dev server** (port 5173) - Frontend with hot-reload
- **Django backend** (port 3000) - API and authentication

#### Option 1: Use the startup script (Recommended)

```bash
./start_server.sh
```

This script:
1. Checks for required dependencies
2. Runs Django migrations
3. Builds the Vue frontend
4. Starts the Django server on port 3000

Access the application at [http://localhost:3000](http://localhost:3000)

#### Option 2: Run servers separately

In one terminal, start the Vite dev server:

```bash
npm run dev
```

In another terminal, start the Django backend:

```bash
cd backend
python3 manage.py runserver 3000
```

- Frontend (Vite): [http://localhost:5173](http://localhost:5173)
- Backend (Django): [http://localhost:3000](http://localhost:3000)
- API Documentation: [http://localhost:3000/api/docs/](http://localhost:3000/api/docs/)
- User Docs: [http://localhost:3000/docs/](http://localhost:3000/docs/)

**Note**: For the full application experience, use port 3000 which serves the built frontend and backend together.

### Production Mode

For production deployment:

```bash
# Build the frontend
npm run build

# Start the Django server
cd backend
python3 manage.py runserver 3000
```

The application will be available at [http://localhost:3000](http://localhost:3000)

## Troubleshooting

### Port Already in Use

If you see an error about port 5173 or 3000 being in use:

```bash
# Find the process using the port (Linux/macOS)
lsof -i :5173
lsof -i :3000

# Kill the process
kill -9 <PID>
```

On Windows:

```cmd
# Find the process
netstat -ano | findstr :5173

# Kill the process
taskkill /PID <PID> /F
```

### Node.js Version Issues

If you encounter version-related errors:

```bash
# Check your Node.js version
node --version

# Update Node.js using nvm (if installed)
nvm install 18
nvm use 18
```

### Python Dependencies Installation Fails

If pip installation fails:

```bash
# Upgrade pip
pip install --upgrade pip

# Try installing with --user flag
pip install --user -r requirements.txt

# Or use a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Database Connection Issues

If you have MySQL connection problems:

1. Verify MySQL is running:
   ```bash
   sudo systemctl status mysql  # Linux
   brew services list           # macOS
   ```

2. Check credentials in `.env`
3. Ensure the database exists:
   ```bash
   mysql -u root -p
   CREATE DATABASE racker;
   ```

### Build Errors

If `npm run build` fails:

```bash
# Clear npm cache
npm cache clean --force

# Remove node_modules and reinstall
rm -rf node_modules
npm install

# Try building again
npm run build
```

## Next Steps

Once installation is complete:

1. Read the [Usage Guide](usage.md) to learn how to use Racker
2. Review [Configuration Options](configuration.md) to customize your setup
3. Explore the [API Documentation](api.md) for programmatic access
4. Check out the [Development Guide](development.md) if you want to contribute

## Uninstalling

To remove Racker from your system:

```bash
# Remove node_modules
rm -rf node_modules

# Remove Python virtual environment (if created)
rm -rf venv

# Remove the entire project directory
cd ..
rm -rf racker
```

## Database Setup (MySQL)

If you want to use the database features for site persistence and authentication:

### 1. Create MySQL Database

```bash
mysql -u root -p
```

In the MySQL prompt:

```sql
CREATE DATABASE racker CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'racker_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON racker.* TO 'racker_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 2. Configure Database in .env

Update your `.env` file:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=racker
DB_USER=racker_user
DB_PASSWORD=your_secure_password
```

### 3. Run Migrations

```bash
cd backend
python3 manage.py migrate
cd ..
```

This creates the necessary tables:
- `api_site` - Site configurations
- `api_rackconfiguration` - Saved rack layouts
- `api_device` - Custom device definitions
- `api_rack` - Individual racks
- `api_rackdevice` - Devices placed in racks
- `auth_user` - User accounts (if authentication enabled)
- `webauthn_*` - Passkey authentication tables

### 4. Create Admin User (Optional)

If you enable authentication, create an admin user:

```bash
cd backend
python3 manage.py createsuperuser
cd ..
```

Follow the prompts to set username, email, and password.

### 5. Access Admin Panel

With authentication enabled, access the Django admin at:
[http://localhost:3000/admin](http://localhost:3000/admin)
```
