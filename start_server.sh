#!/bin/bash
# RackSum Full Stack Server Startup Script
set -e  # Exit on error

echo "=== RackSum Full Stack Setup & Startup ==="

# Step 1: Build Vue Frontend
echo ""
echo "📦 Building Vue.js frontend..."
if [ ! -d "node_modules" ]; then
    echo "🔧 Node modules not found. Installing npm dependencies..."
    npm install
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
if [ ! -f "venv/.dependencies_installed" ]; then
    echo "📦 Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
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

# Step 7: Check for superuser (optional)
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

# Step 8: Start Django server
echo ""
echo "🚀 Starting Django server on port 3000..."
echo "========================================================"
echo "   🌐 Vue App:      http://localhost:3000"
echo "   🔧 Admin Panel:  http://localhost:3000/admin"
echo "   📡 API:          http://localhost:3000/api"
echo ""
echo "   Admin credentials: admin / admin123"
echo ""
echo "   Press Ctrl+C to stop the server"
echo "========================================================"
echo ""
python manage.py runserver 3000
