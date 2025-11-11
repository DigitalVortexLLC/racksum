#!/bin/bash
# RackSum Full Stack Server Startup Script
# Supports both development and production modes
set -e  # Exit on error

# Load environment variables if .env exists
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Determine mode
MODE="${1:-development}"
ENVIRONMENT="${ENVIRONMENT:-development}"

# Use command line argument or environment variable
if [ "$MODE" = "production" ] || [ "$ENVIRONMENT" = "production" ]; then
    MODE="production"
    PORT="${SERVER_PORT:-8000}"
    BIND="${BIND_ADDRESS:-0.0.0.0}"
else
    MODE="development"
    PORT="${SERVER_PORT:-3000}"
    BIND="${BIND_ADDRESS:-127.0.0.1}"
fi

echo "=== RackSum Full Stack Setup & Startup ==="
echo "Mode: ${MODE}"
echo ""

# Step 1: Build Vue Frontend
echo ""
echo "📦 Building Vue.js frontend..."
if [ ! -d "node_modules" ]; then
    echo "🔧 Node modules not found. Installing npm dependencies..."
    if [ "$MODE" = "production" ]; then
        npm install --production
    else
        npm install
    fi
    echo "✓ npm dependencies installed"
fi

echo "🔨 Building production bundle..."
npm run build
echo "✓ Vue app built successfully"

# Step 2: Check and create virtual environment if needed
echo ""
echo "🐍 Setting up Python environment..."
if [ ! -d "venv" ]; then
    echo "🔧 Virtual environment not found. Creating new virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Step 3: Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Step 4: Check if dependencies are installed
if [ ! -f "venv/.dependencies_installed" ] || [ "$MODE" = "production" ]; then
    echo "📦 Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt

    # Install gunicorn for production
    if [ "$MODE" = "production" ]; then
        pip install gunicorn
    fi

    # Create marker file to skip this step on future runs
    touch venv/.dependencies_installed
    echo "✓ Dependencies installed"
else
    echo "✓ Python dependencies already installed"
fi

# Step 5: Navigate to backend directory
cd backend

# Step 6: Run migrations to create/update database
echo ""
echo "🗄️  Running database migrations..."
python manage.py migrate --no-input
echo "✓ Database ready"

# Step 7: Collect static files (production only)
if [ "$MODE" = "production" ]; then
    echo ""
    echo "📁 Collecting static files..."
    python manage.py collectstatic --no-input
    echo "✓ Static files collected"
fi

# Step 8: Check for superuser (optional)
echo ""
echo "👤 Checking for admin user..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✓ Admin user created (username: admin, password: admin123)')
else:
    print('✓ Admin user already exists')
" 2>/dev/null || echo "  (Skipping superuser check)"

# Step 9: Check MCP server configuration
echo ""
if [ -f "../.env" ] && grep -q "MCP_ENABLED=true" ../.env; then
    echo "🤖 MCP Server: ENABLED"
    echo "   The MCP server will start automatically with Django"
    echo "   Available tools: site stats, resource usage, device info"
else
    echo "ℹ️  MCP Server: DISABLED"
    echo "   To enable: Set MCP_ENABLED=true in .env file"
fi

# Step 10: Start server
echo ""

if [ "$MODE" = "production" ]; then
    # Production mode with Gunicorn
    echo "🚀 Starting production server with Gunicorn..."
    echo "========================================================"
    echo "   🌐 Application:  http://${BIND}:${PORT}"
    echo "   🔧 Admin Panel:  http://${BIND}:${PORT}/admin"
    echo "   📡 API:          http://${BIND}:${PORT}/api"
    echo ""
    echo "   Mode: PRODUCTION"
    echo "   Bind: ${BIND}:${PORT}"
    echo ""
    echo "   Press Ctrl+C to stop the server"
    echo "========================================================"
    echo ""

    # Start Gunicorn
    cd ..
    exec gunicorn --config gunicorn.conf.py --chdir backend backend.wsgi:application
else
    # Development mode with Django runserver
    echo "🚀 Starting development server..."
    echo "========================================================"
    echo "   🌐 Vue App:      http://localhost:${PORT}"
    echo "   🔧 Admin Panel:  http://localhost:${PORT}/admin"
    echo "   📡 API:          http://localhost:${PORT}/api"
    echo ""
    echo "   Mode: DEVELOPMENT"
    echo "   Admin credentials: admin / admin123"
    echo ""
    echo "   Press Ctrl+C to stop the server"
    echo "========================================================"
    echo ""

    exec python manage.py runserver ${BIND}:${PORT}
fi
