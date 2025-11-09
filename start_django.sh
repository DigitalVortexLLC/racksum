#!/bin/bash
# RackSum Django Server Startup Script

# Activate virtual environment
source venv/bin/activate

# Run migrations (if needed)
cd backend
python manage.py migrate --no-input

# Start Django server
echo "Starting Django server on port 3000..."
python manage.py runserver 3000
