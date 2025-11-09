# Installation Guide

This guide will walk you through installing and setting up RackSum on your system.

## Prerequisites

Before installing RackSum, ensure you have the following software installed:

### Required Software

- **Node.js**: Version 18 or higher
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
git clone <repository-url>
cd racksum
```

If you downloaded a ZIP file instead:

```bash
# Extract and navigate to the directory
unzip racksum.zip
cd racksum
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
DB_NAME=racksum
DB_USER=your_username
DB_PASSWORD=your_password

# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
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

For development with hot-reload:

```bash
npm run dev
```

The application will be available at [http://localhost:5173](http://localhost:5173)

### Production Mode

For production deployment:

```bash
# Build the frontend
npm run build

# Start the backend server
npm run server
```

Or use the combined command:

```bash
npm start
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
   CREATE DATABASE racksum;
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

1. Read the [Usage Guide](usage.md) to learn how to use RackSum
2. Review [Configuration Options](configuration.md) to customize your setup
3. Explore the [API Documentation](api.md) for programmatic access
4. Check out the [Development Guide](development.md) if you want to contribute

## Uninstalling

To remove RackSum from your system:

```bash
# Remove node_modules
rm -rf node_modules

# Remove Python virtual environment (if created)
rm -rf venv

# Remove the entire project directory
cd ..
rm -rf racksum
```
