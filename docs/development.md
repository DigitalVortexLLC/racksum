# Development Guide

This guide helps you set up a development environment and contribute to RackSum.

## Development Setup

### Prerequisites

Ensure you have installed:

- Node.js 18+
- Python 3.8+
- MySQL 5.7+ (optional)
- Git
- Code editor (VS Code recommended)

### Clone and Install

```bash
# Clone the repository
git clone <repository-url>
cd racksum

# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
```

### Development Environment

```bash
# Start frontend dev server (with hot reload)
npm run dev

# In another terminal, start backend
npm run server
```

Frontend: [http://localhost:5173](http://localhost:5173)
Backend API: [http://localhost:3000](http://localhost:3000)

## Project Structure

```
racksum/
├── backend/                 # Django backend
│   ├── api/                # REST API app
│   │   ├── models.py       # Data models
│   │   ├── serializers.py  # API serializers
│   │   ├── views.py        # API views
│   │   └── urls.py         # URL routing
│   ├── backend/            # Django project settings
│   │   ├── settings.py     # Configuration
│   │   ├── urls.py         # Main URL config
│   │   └── wsgi.py         # WSGI config
│   └── manage.py           # Django management
├── src/                    # Vue frontend
│   ├── components/         # Vue components
│   │   ├── DeviceLibrary.vue
│   │   ├── Rack.vue
│   │   ├── RackContainer.vue
│   │   ├── UnrackedDevices.vue
│   │   ├── UtilizationPanel.vue
│   │   └── ...
│   ├── composables/        # Vue composables
│   │   ├── useDevices.js
│   │   ├── useDragDrop.js
│   │   ├── useRackConfig.js
│   │   └── useUtilization.js
│   ├── data/              # Static data
│   │   └── devices.json   # Device library
│   ├── db/                # Database utilities
│   │   ├── connection.js
│   │   ├── schema.sql
│   │   └── services.js
│   ├── utils/             # Utility functions
│   │   ├── calculations.js
│   │   └── validators.js
│   ├── assets/            # Styles and static assets
│   ├── App.vue            # Root component
│   └── main.js            # Entry point
├── docs/                  # MkDocs documentation
├── public/                # Public static files
├── dist/                  # Build output
├── server.js              # Legacy Express server
├── package.json           # Node dependencies
├── requirements.txt       # Python dependencies
├── vite.config.js         # Vite configuration
├── tailwind.config.js     # Tailwind configuration
└── mkdocs.yml            # MkDocs configuration
```

## Frontend Development

### Vue 3 Composition API

RackSum uses Vue 3 with the Composition API.

#### Example Component

```vue
<script setup>
import { ref, computed } from 'vue';
import { useDevices } from '@/composables/useDevices';

const { devices, loadDevices } = useDevices();
const selectedCategory = ref('all');

const filteredDevices = computed(() => {
  if (selectedCategory.value === 'all') {
    return devices.value;
  }
  return devices.value.filter(d => d.category === selectedCategory.value);
});
</script>

<template>
  <div class="device-list">
    <div v-for="device in filteredDevices" :key="device.id">
      {{ device.name }}
    </div>
  </div>
</template>
```

### Composables

Composables provide reusable stateful logic.

#### useDevices.js

Manages device library state:

```javascript
import { ref } from 'vue';

export function useDevices() {
  const devices = ref([]);
  const loading = ref(false);

  async function loadDevices() {
    loading.value = true;
    try {
      const response = await fetch('/api/devices');
      devices.value = await response.json();
    } finally {
      loading.value = false;
    }
  }

  return { devices, loading, loadDevices };
}
```

#### useRackConfig.js

Manages rack configuration state:

```javascript
import { ref, computed } from 'vue';

export function useRackConfig() {
  const racks = ref([]);
  const settings = ref({
    totalPowerCapacity: 10000,
    hvacCapacity: 10,
    ruPerRack: 42
  });

  const totalPowerUsage = computed(() => {
    return racks.value.reduce((total, rack) => {
      return total + rack.devices.reduce((sum, d) => sum + d.powerDraw, 0);
    }, 0);
  });

  return { racks, settings, totalPowerUsage };
}
```

### Styling with Tailwind CSS

Use Tailwind utility classes:

```vue
<template>
  <div class="flex items-center justify-between p-4 bg-gray-100 rounded-lg">
    <h2 class="text-xl font-bold text-gray-800">Device Library</h2>
    <button class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
      Add Device
    </button>
  </div>
</template>
```

### PrimeVue Components

RackSum uses PrimeVue for UI components:

```vue
<script setup>
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import { ref } from 'vue';

const visible = ref(false);
</script>

<template>
  <Button label="Open Dialog" @click="visible = true" />
  <Dialog v-model:visible="visible" header="Configuration">
    <p>Dialog content here</p>
  </Dialog>
</template>
```

### Drag and Drop

Using VueUse for drag and drop:

```javascript
import { useDraggable, useDropZone } from '@vueuse/core';

export function useDragDrop() {
  const { isDragging, position } = useDraggable(dragElement);

  const { isOverDropZone } = useDropZone(dropElement, {
    onDrop: (files, event) => {
      // Handle drop
    }
  });

  return { isDragging, position, isOverDropZone };
}
```

## Backend Development

### Django Models

Define data models in `backend/api/models.py`:

```python
from django.db import models

class RackConfiguration(models.Model):
    config_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_power_capacity = models.IntegerField()
    hvac_capacity = models.FloatField()
    ru_per_rack = models.IntegerField(default=42)

    def __str__(self):
        return self.name

class Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    ru_size = models.IntegerField()
    power_draw = models.IntegerField()
    color = models.CharField(max_length=7)

    def __str__(self):
        return self.name
```

### API Views

Create API endpoints in `backend/api/views.py`:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Device
from .serializers import DeviceSerializer

@api_view(['GET'])
def get_devices(request):
    devices = Device.objects.all()
    serializer = DeviceSerializer(devices, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def load_configuration(request):
    try:
        config = request.data
        # Process configuration
        return Response({
            'success': True,
            'message': 'Configuration loaded successfully'
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
```

### Serializers

Define serializers in `backend/api/serializers.py`:

```python
from rest_framework import serializers
from .models import Device, RackConfiguration

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class RackConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RackConfiguration
        fields = '__all__'
```

### URL Routing

Configure routes in `backend/api/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('devices/', views.get_devices, name='get_devices'),
    path('load/', views.load_configuration, name='load_configuration'),
    path('save/', views.save_configuration, name='save_configuration'),
]
```

## Testing

### Frontend Testing

Install testing dependencies:

```bash
npm install -D @vue/test-utils vitest
```

Create test file `src/components/__tests__/DeviceLibrary.test.js`:

```javascript
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import DeviceLibrary from '../DeviceLibrary.vue';

describe('DeviceLibrary', () => {
  it('renders devices', () => {
    const wrapper = mount(DeviceLibrary, {
      props: {
        devices: [
          { id: '1', name: 'Test Device', powerDraw: 100 }
        ]
      }
    });

    expect(wrapper.text()).toContain('Test Device');
  });
});
```

Run tests:

```bash
npm run test
```

### Backend Testing

Create test file `backend/api/tests.py`:

```python
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Device

class DeviceAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        Device.objects.create(
            device_id='test-1',
            name='Test Device',
            category='network',
            ru_size=1,
            power_draw=100,
            color='#000000'
        )

    def test_get_devices(self):
        response = self.client.get('/api/devices/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_load_configuration(self):
        config = {
            'settings': {
                'totalPowerCapacity': 10000,
                'hvacCapacity': 10,
                'ruPerRack': 42
            },
            'racks': []
        }
        response = self.client.post('/api/load/', config, format='json')
        self.assertEqual(response.status_code, 200)
```

Run tests:

```bash
cd backend
python manage.py test
```

## Code Quality

### Linting

Frontend (ESLint):

```bash
# Install ESLint
npm install -D eslint @vue/eslint-config-prettier

# Run linter
npm run lint
```

Backend (Flake8):

```bash
# Install flake8
pip install flake8

# Run linter
flake8 backend/
```

### Code Formatting

Frontend (Prettier):

```bash
# Install Prettier
npm install -D prettier

# Format code
npx prettier --write "src/**/*.{js,vue}"
```

Backend (Black):

```bash
# Install Black
pip install black

# Format code
black backend/
```

## Git Workflow

### Branching Strategy

```bash
# Create feature branch
git checkout -b feature/add-new-device-type

# Make changes and commit
git add .
git commit -m "Add support for blade server devices"

# Push to remote
git push origin feature/add-new-device-type

# Create pull request on GitHub
```

### Commit Messages

Follow conventional commits:

```
feat: add support for custom device colors
fix: correct HVAC capacity calculation
docs: update API documentation
refactor: simplify drag and drop logic
test: add tests for utilization calculations
```

## Debugging

### Frontend Debugging

Use Vue DevTools browser extension:

1. Install Vue DevTools
2. Open DevTools (F12)
3. Navigate to Vue tab
4. Inspect component state and events

Console logging:

```javascript
console.log('Debug:', { devices, racks, settings });
```

### Backend Debugging

Django Debug Toolbar:

```bash
pip install django-debug-toolbar
```

Add to `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ...
]

INTERNAL_IPS = ['127.0.0.1']
```

Python debugger:

```python
import pdb; pdb.set_trace()
```

## Performance Optimization

### Frontend Optimization

1. **Lazy Loading**

```javascript
// Lazy load components
const DeviceLibrary = defineAsyncComponent(() =>
  import('./components/DeviceLibrary.vue')
);
```

2. **Virtual Scrolling**

For long lists:

```bash
npm install vue-virtual-scroller
```

3. **Memoization**

```javascript
import { computed, ref } from 'vue';

const expensiveComputation = computed(() => {
  // Cached until dependencies change
  return devices.value.map(/* ... */);
});
```

### Backend Optimization

1. **Database Queries**

```python
# Use select_related for foreign keys
devices = Device.objects.select_related('category').all()

# Use prefetch_related for many-to-many
racks = Rack.objects.prefetch_related('devices').all()
```

2. **Caching**

```python
from django.core.cache import cache

def get_devices():
    devices = cache.get('devices')
    if devices is None:
        devices = Device.objects.all()
        cache.set('devices', devices, 3600)  # Cache for 1 hour
    return devices
```

## Adding New Features

### Example: Add New Device Category

1. **Update Device Library**

Edit `src/data/devices.json`:

```json
{
  "categories": [
    {
      "id": "cooling",
      "name": "Cooling Equipment",
      "devices": [
        {
          "id": "ac-unit-1",
          "name": "In-Row Cooling Unit",
          "category": "cooling",
          "ruSize": 3,
          "powerDraw": 2000,
          "color": "#00BCD4"
        }
      ]
    }
  ]
}
```

2. **Update Backend Model** (if needed)

```python
DEVICE_CATEGORIES = [
    ('power', 'Power'),
    ('network', 'Network'),
    ('servers', 'Servers'),
    ('storage', 'Storage'),
    ('specialized', 'Specialized'),
    ('cooling', 'Cooling'),  # New category
]
```

3. **Test the Feature**

```bash
# Reload frontend
npm run dev

# Verify in UI
```

## Contributing

### Contribution Workflow

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit pull request

### Pull Request Guidelines

- Clear description of changes
- Tests for new features
- Documentation updates
- Follow code style guidelines
- Link to related issues

## Resources

### Documentation

- [Vue 3 Documentation](https://vuejs.org/)
- [Django Documentation](https://docs.djangoproject.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [PrimeVue Documentation](https://primevue.org/)
- [VueUse Documentation](https://vueuse.org/)

### Tools

- [Vue DevTools](https://devtools.vuejs.org/)
- [VS Code](https://code.visualstudio.com/)
- [Postman](https://www.postman.com/) for API testing
- [Git](https://git-scm.com/)

## Getting Help

- Check existing documentation
- Search GitHub issues
- Ask questions in discussions
- Review code examples in the repository

## Next Steps

- Review [Usage Guide](usage.md)
- Explore [API Documentation](api.md)
- Check [Configuration Options](configuration.md)
