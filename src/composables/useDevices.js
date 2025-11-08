import { ref, onMounted } from 'vue'

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

      categories.value = devicesData.categories || []
    } catch (err) {
      console.error('Failed to load devices:', err)
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  // Load devices on mount
  onMounted(() => {
    if (categories.value.length === 0) {
      loadDevices()
    }
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