import { ref, watch } from 'vue'

const STORAGE_KEY = 'racksum-config'

// Default configuration
const createDefaultConfig = () => ({
  configId: `config-${Date.now()}`,
  metadata: {
    createdAt: new Date().toISOString(),
    lastModified: new Date().toISOString(),
    description: 'Rack configuration'
  },
  settings: {
    totalPowerCapacity: 10000,
    hvacCapacity: 34100, // ~10kW in BTU/hr (1W = 3.41 BTU/hr)
    ruPerRack: 42
  },
  racks: [
    {
      id: 'rack-1',
      name: 'Rack 1',
      devices: []
    }
  ],
  unrackedDevices: [] // Devices without rack assignments
})

// Global state
const config = ref(createDefaultConfig())

// Load from localStorage on init
const loadFromStorage = () => {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      config.value = JSON.parse(saved)
    }
  } catch (error) {
    console.error('Failed to load configuration from localStorage:', error)
  }
}

// Save to localStorage on change
watch(config, (newConfig) => {
  try {
    newConfig.metadata.lastModified = new Date().toISOString()
    localStorage.setItem(STORAGE_KEY, JSON.stringify(newConfig))
  } catch (error) {
    console.error('Failed to save configuration to localStorage:', error)
  }
}, { deep: true })

// Initialize on first load
loadFromStorage()

export function useRackConfig() {
  const racks = ref(config.value.racks)
  const unrackedDevices = ref(config.value.unrackedDevices || [])

  // Update racks and unracked devices when config changes
  watch(config, (newConfig) => {
    racks.value = newConfig.racks
    unrackedDevices.value = newConfig.unrackedDevices || []
  }, { deep: true })

  const updateSettings = (newSettings) => {
    config.value.settings = {
      ...config.value.settings,
      ...newSettings
    }
  }

  const initializeRacks = (numberOfRacks) => {
    const currentCount = config.value.racks.length

    if (numberOfRacks > currentCount) {
      // Add racks
      for (let i = currentCount; i < numberOfRacks; i++) {
        config.value.racks.push({
          id: `rack-${i + 1}`,
          name: `Rack ${i + 1}`,
          devices: []
        })
      }
    } else if (numberOfRacks < currentCount) {
      // Remove racks
      config.value.racks = config.value.racks.slice(0, numberOfRacks)
    }
  }

  const updateRack = (rackId, updates) => {
    const rack = config.value.racks.find(r => r.id === rackId)
    if (rack) {
      Object.assign(rack, updates)
    }
  }

  const addDeviceToRack = (rackId, device, position) => {
    const rack = config.value.racks.find(r => r.id === rackId)
    if (!rack) return false

    // Check if position is valid and has enough space
    if (!canPlaceDevice(rackId, position, device.ruSize)) {
      return false
    }

    // Create device instance (or use existing if it has instanceId)
    const deviceInstance = {
      ...device,
      position,
      instanceId: device.instanceId || `${device.id}-${Date.now()}`,
      customName: device.customName || device.name
    }

    // If device was in unracked, remove it from there
    if (device.instanceId) {
      config.value.unrackedDevices = config.value.unrackedDevices.filter(
        d => d.instanceId !== device.instanceId
      )
    }

    rack.devices.push(deviceInstance)
    return true
  }

  const canPlaceDevice = (rackId, position, ruSize, excludeInstanceId = null) => {
    const rack = config.value.racks.find(r => r.id === rackId)
    if (!rack) return false

    const maxRU = config.value.settings.ruPerRack

    // Check if device would exceed rack height
    if (position + ruSize - 1 > maxRU) {
      return false
    }

    // Check for overlapping devices
    const endPosition = position + ruSize - 1
    for (const device of rack.devices) {
      // Skip the device we're moving (if any)
      if (excludeInstanceId && device.instanceId === excludeInstanceId) {
        continue
      }

      const deviceEnd = device.position + device.ruSize - 1

      // Check if ranges overlap
      if (!(endPosition < device.position || position > deviceEnd)) {
        return false
      }
    }

    return true
  }

  const removeDeviceFromRack = (rackId, instanceId) => {
    const rack = config.value.racks.find(r => r.id === rackId)
    if (!rack) return

    rack.devices = rack.devices.filter(d => d.instanceId !== instanceId)
  }

  const addUnrackedDevice = (device) => {
    // Ensure unrackedDevices array exists
    if (!config.value.unrackedDevices) {
      config.value.unrackedDevices = []
    }

    // Create device instance with unique ID
    const deviceInstance = {
      ...device,
      instanceId: device.instanceId || `${device.id}-${Date.now()}`,
      customName: device.customName || device.name
    }

    config.value.unrackedDevices.push(deviceInstance)
  }

  const removeUnrackedDevice = (instanceId) => {
    if (!config.value.unrackedDevices) return

    config.value.unrackedDevices = config.value.unrackedDevices.filter(
      d => d.instanceId !== instanceId
    )
  }

  const loadConfiguration = (newConfig) => {
    // Validate basic structure
    if (!newConfig.settings || !newConfig.racks) {
      throw new Error('Invalid configuration structure')
    }

    // Process devices without position/rack and put them in unracked
    const unracked = []

    if (newConfig.devices && Array.isArray(newConfig.devices)) {
      // Handle flat device list (devices without rack assignment)
      newConfig.devices.forEach(device => {
        if (!device.position || !device.rackId) {
          unracked.push({
            ...device,
            instanceId: device.instanceId || `${device.id}-${Date.now()}`,
            customName: device.customName || device.name
          })
        }
      })
    }

    config.value = {
      ...newConfig,
      unrackedDevices: newConfig.unrackedDevices || unracked,
      metadata: {
        ...newConfig.metadata,
        lastModified: new Date().toISOString()
      }
    }
  }

  const resetConfiguration = () => {
    config.value = createDefaultConfig()
  }

  return {
    config,
    racks,
    unrackedDevices,
    updateSettings,
    initializeRacks,
    updateRack,
    addDeviceToRack,
    canPlaceDevice,
    removeDeviceFromRack,
    addUnrackedDevice,
    removeUnrackedDevice,
    loadConfiguration,
    resetConfiguration
  }
}