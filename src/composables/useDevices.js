import { ref, onMounted, onUnmounted } from 'vue'
import { logError, logWarn, logInfo, logDebug } from '../utils/logger'

const categories = ref([])
const loading = ref(false)
const error = ref(null)

export function useDevices() {
  const loadDevices = async () => {
    loading.value = true
    error.value = null

    try {
      // Try to load from API first (production)
      let devicesData
      try {
        const response = await fetch('/api/devices')
        if (response.ok) {
          devicesData = await response.json()
        }
      } catch (apiError) {
        // Fallback to importing from local file (development)
        const module = await import('../data/devices.json')
        devicesData = module.default
      }

      // Load default devices
      const defaultCategories = devicesData.categories || []
      
      // Load custom device groups from localStorage
      const savedGroups = localStorage.getItem('racker-device-groups')
      let customGroups = []
      if (savedGroups) {
        try {
          customGroups = JSON.parse(savedGroups)
        } catch (err) {
          logError('Error loading custom device groups', err)
        }
      }

      // Load custom devices from localStorage
      const savedDevices = localStorage.getItem('racker-custom-devices')
      let customDevices = []
      if (savedDevices) {
        try {
          customDevices = JSON.parse(savedDevices)
        } catch (err) {
          logError('Error loading custom devices', err)
        }
      }

      // Merge categories: start with default categories
      const mergedCategories = [...defaultCategories]

      // Add custom groups that don't exist in defaults
      customGroups.forEach(group => {
        const existingCategory = mergedCategories.find(cat => 
          cat.name.toLowerCase() === group.name.toLowerCase()
        )
        
        if (!existingCategory) {
          mergedCategories.push({
            id: group.id,
            name: group.name,
            devices: []
          })
        }
      })

      // Add custom devices to their respective categories
      customDevices.forEach(device => {
        const category = mergedCategories.find(cat => 
          cat.name.toLowerCase() === device.category.toLowerCase()
        )
        
        if (category) {
          // Check if device already exists to avoid duplicates
          const existingDevice = category.devices.find(d => d.id === device.id)
          if (!existingDevice) {
            category.devices.push(device)
          }
        }
      })

      categories.value = mergedCategories
    } catch (err) {
      logError('Failed to load devices', err)
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  // Listen for custom events to reload devices
  const handleDevicesUpdated = () => {
    loadDevices()
  }

  // Load devices on mount
  onMounted(() => {
    if (categories.value.length === 0) {
      loadDevices()
    }
    // Listen for device updates
    window.addEventListener('devices-updated', handleDevicesUpdated)
  })

  onUnmounted(() => {
    window.removeEventListener('devices-updated', handleDevicesUpdated)
  })

  const getDeviceById = (deviceId) => {
    for (const category of categories.value) {
      const device = category.devices.find(d => d.id === deviceId)
      if (device) return device
    }
    return null
  }

  return {
    categories,
    loading,
    error,
    loadDevices,
    getDeviceById
  }
}