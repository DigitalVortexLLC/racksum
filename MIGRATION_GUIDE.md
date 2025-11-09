# Migration from Express to Django

This document describes the migration from Express.js to Django for the RackSum backend.

## Changes Made

### Backend Migration

1. **Django Project Structure**
   - Created `backend/` directory with Django project
   - Created `api/` app for all API endpoints
   - Maintained compatibility with existing database schema

2. **Database Models** (`backend/api/models.py`)
   - `Site` model: Matches existing `sites` table
   - `RackConfiguration` model: Matches existing `rack_configurations` table
   - Uses existing MySQL database (no schema changes required)

3. **API Endpoints**
   All Express endpoints have been migrated to Django REST Framework:

   | Endpoint | Method | Express | Django |
   |----------|--------|---------|--------|
   | `/api/load` | POST | ✓ | ✓ |
   | `/api/devices` | GET | ✓ | ✓ |
   | `/api/sites` | GET | ✓ | ✓ |
   | `/api/sites/:id` | GET | ✓ | ✓ |
   | `/api/sites` | POST | ✓ | ✓ |
   | `/api/sites/:id` | PUT | ✓ | ✓ |
   | `/api/sites/:id` | DELETE | ✓ | ✓ |
   | `/api/sites/:siteId/racks` | GET | ✓ | ✓ |
   | `/api/sites/:siteId/racks` | POST | ✓ | ✓ |
   | `/api/sites/:siteId/racks/:rackName` | GET | ✓ | ✓ |
   | `/api/racks/:id` | DELETE | ✓ | ✓ |
   | `/api/racks` | GET | ✓ | ✓ |

4. **Configuration**
   - CORS enabled for development
   - MySQL database connection using PyMySQL
   - Static file serving for Vue build
   - Environment variable support via python-dotenv

### Files Modified

- `package.json`: Updated to use Django
  - `npm run server`: Runs Django server
  - `npm run db:init`: Runs Django migrations
  - Removed Express dependencies (express, cors, mysql2, dotenv)

### New Files Created

- `backend/` - Django project directory
  - `backend/settings.py` - Django configuration
  - `backend/urls.py` - Main URL routing
  - `api/models.py` - Database models
  - `api/serializers.py` - DRF serializers
  - `api/views.py` - API views
  - `api/urls.py` - API URL routing
  - `api/migrations/` - Database migrations
- `requirements.txt` - Python dependencies
- `venv/` - Python virtual environment
- `start_server.sh` - Server startup script

### Files Removed (Post-Migration Cleanup)

- `server.js` - Original Express server (no longer needed)
- `src/db/` - Original Express database code (replaced by Django models)
  - `src/db/connection.js`
  - `src/db/services.js`
  - `src/db/init.js`
  - `src/db/schema.sql`
- `src/composables/useDatabase_new.js` - Duplicate file (removed)

## Setup Instructions

### First Time Setup

1. **Install Python Dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Database**
   Create a `.env` file in the project root with your MySQL credentials:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=racksum
   DB_PORT=3306
   ```

3. **Run Migrations**
   ```bash
   cd backend
   python manage.py migrate
   ```

4. **Build Frontend**
   ```bash
   npm install
   npm run build
   ```

### Running the Application

**Option 1: Using npm scripts**
```bash
npm run server
```

**Option 2: Using the startup script**
```bash
chmod +x start_django.sh
./start_django.sh
```

**Option 3: Manual startup**
```bash
source venv/bin/activate
cd backend
python manage.py runserver 3000
```

The server will be available at `http://localhost:3000`

## Development

### Frontend Development
```bash
npm run dev  # Vite dev server on port 5173
```

### Backend Development
```bash
source venv/bin/activate
cd backend
python manage.py runserver 3000
```

## Testing

The Django server provides the exact same API interface as Express, so the frontend requires **no changes** and will work seamlessly with the new backend.

## Database

Django uses the **existing MySQL database** - no schema changes were required. The models were designed to match the existing table structure exactly:
- Table names: `sites`, `rack_configurations`
- All columns, indexes, and constraints preserved
- Foreign key relationships maintained

## Compatibility

- ✓ All API endpoints maintained
- ✓ Same request/response formats
- ✓ Same error handling
- ✓ Same database schema
- ✓ Frontend requires no changes
- ✓ Same port (3000) by default

## Benefits of Django

1. **Better ORM**: Django's ORM provides better type safety and query optimization
2. **Admin Interface**: Built-in admin panel at `/admin/`
3. **Migrations**: Database schema version control
4. **REST Framework**: Powerful serialization and validation
5. **Security**: Built-in protection against common vulnerabilities
6. **Scalability**: Better performance for complex queries
7. **Ecosystem**: Rich ecosystem of packages and tools

## Migration Complete

The migration from Express to Django is now complete. All legacy Express files have been removed from the codebase. The application now runs exclusively on Django.

If you need to reference the old Express implementation, you can find it in the git history before the post-migration cleanup commit.
