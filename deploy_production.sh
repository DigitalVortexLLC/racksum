#!/bin/bash
# Racker Production Deployment Script
# This script sets up Racker for production deployment with systemd

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="/opt/racker"
SERVICE_NAME="racker"
SERVICE_USER="www-data"
SERVICE_GROUP="www-data"

echo -e "${BLUE}=== Racker Production Deployment ===${NC}"
echo ""

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}Error: This script must be run as root (use sudo)${NC}"
   exit 1
fi

# Check if systemd is available
if ! command -v systemctl &> /dev/null; then
    echo -e "${RED}Error: systemd is not available on this system${NC}"
    echo "This deployment script requires systemd"
    exit 1
fi

# Ask for confirmation
echo -e "${YELLOW}This script will:${NC}"
echo "  - Install Racker to ${INSTALL_DIR}"
echo "  - Create systemd service as ${SERVICE_NAME}"
echo "  - Run as user ${SERVICE_USER}"
echo ""
read -p "Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled"
    exit 0
fi

# Step 1: Check prerequisites
echo -e "${BLUE}[1/10] Checking prerequisites...${NC}"
MISSING_DEPS=()

if ! command -v python3 &> /dev/null; then
    MISSING_DEPS+=("python3")
fi

if ! command -v node &> /dev/null; then
    MISSING_DEPS+=("nodejs")
fi

if ! command -v npm &> /dev/null; then
    MISSING_DEPS+=("npm")
fi

if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
    echo -e "${RED}Error: Missing required dependencies: ${MISSING_DEPS[*]}${NC}"
    echo "Please install them first"
    exit 1
fi
echo -e "${GREEN}✓ Prerequisites check passed${NC}"

# Step 2: Create service user if it doesn't exist
echo -e "${BLUE}[2/10] Setting up service user...${NC}"
if ! id -u ${SERVICE_USER} &> /dev/null; then
    echo "Creating user ${SERVICE_USER}..."
    useradd --system --no-create-home --shell /bin/false ${SERVICE_USER}
    echo -e "${GREEN}✓ User created${NC}"
else
    echo -e "${GREEN}✓ User already exists${NC}"
fi

# Step 3: Create installation directory
echo -e "${BLUE}[3/10] Creating installation directory...${NC}"
mkdir -p ${INSTALL_DIR}

# Step 4: Copy application files
echo -e "${BLUE}[4/10] Copying application files...${NC}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copy all files except node_modules, venv, and .git
rsync -av --exclude='node_modules' \
          --exclude='venv' \
          --exclude='backend/venv' \
          --exclude='.git' \
          --exclude='dist' \
          --exclude='*.pyc' \
          --exclude='__pycache__' \
          --exclude='.env' \
          "${SCRIPT_DIR}/" "${INSTALL_DIR}/"

echo -e "${GREEN}✓ Files copied${NC}"

# Step 5: Set up environment file
echo -e "${BLUE}[5/10] Setting up environment configuration...${NC}"
if [ ! -f "${INSTALL_DIR}/.env" ]; then
    cp "${INSTALL_DIR}/.env.example" "${INSTALL_DIR}/.env"
    echo -e "${YELLOW}⚠ Created .env from template${NC}"
    echo -e "${YELLOW}⚠ IMPORTANT: Edit ${INSTALL_DIR}/.env with your production settings!${NC}"

    # Set production defaults
    sed -i 's/ENVIRONMENT=development/ENVIRONMENT=production/' "${INSTALL_DIR}/.env"
    sed -i 's/SERVER_PORT=3000/SERVER_PORT=8000/' "${INSTALL_DIR}/.env"
    sed -i 's/BIND_ADDRESS=127.0.0.1/BIND_ADDRESS=0.0.0.0/' "${INSTALL_DIR}/.env"
    sed -i 's/SENTRY_ENVIRONMENT=development/SENTRY_ENVIRONMENT=production/' "${INSTALL_DIR}/.env"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Step 6: Install Node.js dependencies and build frontend
echo -e "${BLUE}[6/10] Building Vue.js frontend...${NC}"
cd "${INSTALL_DIR}"
npm install --production
npm run build
echo -e "${GREEN}✓ Frontend built${NC}"

# Step 7: Set up Python virtual environment
echo -e "${BLUE}[7/10] Setting up Python virtual environment...${NC}"
python3 -m venv "${INSTALL_DIR}/venv"
source "${INSTALL_DIR}/venv/bin/activate"
pip install --upgrade pip
pip install -r "${INSTALL_DIR}/requirements.txt"
pip install gunicorn
echo -e "${GREEN}✓ Python environment ready${NC}"

# Step 8: Run Django setup
echo -e "${BLUE}[8/10] Configuring Django application...${NC}"
cd "${INSTALL_DIR}/backend"

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate --no-input

# Create superuser if needed
echo -e "${YELLOW}Creating admin superuser...${NC}"
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✓ Admin user created (username: admin, password: admin123)')
    print('⚠ CHANGE THE PASSWORD IMMEDIATELY!')
else:
    print('✓ Admin user already exists')
" 2>/dev/null || echo "  (Superuser setup skipped)"

echo -e "${GREEN}✓ Django configured${NC}"

# Step 9: Set file permissions
echo -e "${BLUE}[9/10] Setting file permissions...${NC}"
chown -R ${SERVICE_USER}:${SERVICE_GROUP} ${INSTALL_DIR}
chmod -R 755 ${INSTALL_DIR}
chmod 600 ${INSTALL_DIR}/.env
echo -e "${GREEN}✓ Permissions set${NC}"

# Step 10: Install and enable systemd service
echo -e "${BLUE}[10/10] Installing systemd service...${NC}"

# Update service file with actual paths
sed -e "s|/opt/racker|${INSTALL_DIR}|g" \
    -e "s|User=www-data|User=${SERVICE_USER}|g" \
    -e "s|Group=www-data|Group=${SERVICE_GROUP}|g" \
    "${INSTALL_DIR}/racker.service" > "/etc/systemd/system/${SERVICE_NAME}.service"

# Reload systemd
systemctl daemon-reload

# Enable service
systemctl enable ${SERVICE_NAME}.service

echo -e "${GREEN}✓ Systemd service installed${NC}"

# Summary
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Production deployment completed!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo ""
echo "1. Edit the configuration file:"
echo "   ${YELLOW}sudo nano ${INSTALL_DIR}/.env${NC}"
echo ""
echo "2. Update these important settings:"
echo "   - Database credentials (if using MySQL)"
echo "   - WebAuthn configuration (WEBAUTHN_RP_ID, WEBAUTHN_ORIGIN)"
echo "   - Sentry DSN (optional)"
echo ""
echo "3. Start the service:"
echo "   ${YELLOW}sudo systemctl start ${SERVICE_NAME}${NC}"
echo ""
echo "4. Check service status:"
echo "   ${YELLOW}sudo systemctl status ${SERVICE_NAME}${NC}"
echo ""
echo "5. View logs:"
echo "   ${YELLOW}sudo journalctl -u ${SERVICE_NAME} -f${NC}"
echo ""
echo "6. Enable service to start on boot:"
echo "   ${YELLOW}sudo systemctl enable ${SERVICE_NAME}${NC}"
echo ""
echo "7. Set up nginx/apache reverse proxy to forward to:"
echo "   ${YELLOW}http://localhost:8000${NC}"
echo ""
echo -e "${RED}IMPORTANT SECURITY:${NC}"
echo "  - Change admin password: http://localhost:8000/admin"
echo "  - Review firewall rules"
echo "  - Set up HTTPS with Let's Encrypt"
echo ""
