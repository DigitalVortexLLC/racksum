import { ref, watch } from 'vue'
import { useDatabase } from './useDatabase'
import { useResourceProviders } from './useResourceProviders'

const STORAGE_KEY = 'racker-config'

// Debounce timer for auto-save
let autoSaveTimer = null
const AUTO_SAVE_DELAY = 2000 // 2 seconds delay

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
    hvacCapacity: 36000, // 3 Refrigeration Tons (1 ton = 12,000 BTU/hr)
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

// Auto-save to database with debouncing (only if site and rack are loaded)
watch(config, (newConfig) => {
  const { currentSite, currentRackName, autoSaveRackConfiguration } = useDatabase()

  // Only auto-save if we have a current site and rack name
  if (!currentSite.value || !currentRackName.value) {
    return
  }

  // Clear existing timer
  if (autoSaveTimer) {
    clearTimeout(autoSaveTimer)
  }

  // Set new timer for debounced auto-save
  autoSaveTimer = setTimeout(() => {
    console.log(`Auto-saving "${currentRackName.value}" to site "${currentSite.value.name}"`)
    autoSaveRackConfiguration(newConfig)
  }, AUTO_SAVE_DELAY)
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
          ruSize: config.value.settings.ruPerRack, // Use global default
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

    // Use rack-specific RU size if available, otherwise fall back to global setting
    const maxRU = rack.ruSize || config.value.settings.ruPerRack

    // Check if device would exceed rack height
    if (position + ruSize - 1 > maxRU) {
      return false
    }

    const endPosition = position + ruSize - 1

    // Check for overlapping devices
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

    // Check for overlapping providers
    const { getProvidersForRack } = useResourceProviders()
    const providers = getProvidersForRack(rackId)
    for (const provider of providers) {
      const providerEnd = provider.position + provider.ruSize - 1

      // Check if ranges overlap
      if (!(endPosition < provider.position || position > providerEnd)) {
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

    // Ensure all racks have ruSize property (for backward compatibility)
    const racksWithRuSize = newConfig.racks.map(rack => ({
      ...rack,
      ruSize: rack.ruSize || newConfig.settings.ruPerRack || 42
    }))

    config.value = {
      ...newConfig,
      racks: racksWithRuSize,
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

  const addRack = () => {
    const rackCount = config.value.racks.length
    const newRack = {
      id: `rack-${Date.now()}`,
      name: `Rack ${rackCount + 1}`,
      ruSize: config.value.settings.ruPerRack, // Use global default
      devices: []
    }
    config.value.racks.push(newRack)
    return newRack
  }

  const deleteRack = (rackId, moveDevicesToUnracked = true) => {
    const rack = config.value.racks.find(r => r.id === rackId)
    if (!rack) return false

    if (moveDevicesToUnracked && rack.devices.length > 0) {
      // Move all devices to unracked
      if (!config.value.unrackedDevices) {
        config.value.unrackedDevices = []
      }
      rack.devices.forEach(device => {
        config.value.unrackedDevices.push({
          ...device,
          position: undefined // Remove position info
        })
      })
    }

    // Remove the rack
    config.value.racks = config.value.racks.filter(r => r.id !== rackId)
    return true
  }

  const reorderRacks = (fromIndex, toIndex) => {
    if (fromIndex === toIndex) return
    if (fromIndex < 0 || fromIndex >= config.value.racks.length) return
    if (toIndex < 0 || toIndex >= config.value.racks.length) return

    const newRacks = [...config.value.racks]
    const [movedRack] = newRacks.splice(fromIndex, 1)
    newRacks.splice(toIndex, 0, movedRack)
    config.value.racks = newRacks
  }

  // Provider placement functions
  const canPlaceProvider = (rackId, position, ruSize, excludeProviderId = null) => {
    const rack = config.value.racks.find(r => r.id === rackId)
    if (!rack) return false

    // Use rack-specific RU size if available, otherwise fall back to global setting
    const maxRU = rack.ruSize || config.value.settings.ruPerRack

    // Check if provider would exceed rack height
    if (position + ruSize - 1 > maxRU) {
      return false
    }

    const endPosition = position + ruSize - 1

    // Check for overlapping devices
    for (const device of rack.devices) {
      const deviceEnd = device.position + device.ruSize - 1

      // Check if ranges overlap
      if (!(endPosition < device.position || position > deviceEnd)) {
        return false
      }
    }

    // Check for overlapping providers
    const { getProvidersForRack } = useResourceProviders()
    const providers = getProvidersForRack(rackId)
    for (const provider of providers) {
      // Skip the provider we're moving (if any)
      if (excludeProviderId && provider.id === excludeProviderId) {
        continue
      }

      const providerEnd = provider.position + provider.ruSize - 1

      // Check if ranges overlap
      if (!(endPosition < provider.position || position > providerEnd)) {
        return false
      }
    }

    return true
  }

  const addProviderToRack = (rackId, providerId, position) => {
    const { getProviderById, placeProviderInRack } = useResourceProviders()
    const provider = getProviderById(providerId)

    if (!provider || !provider.ruSize || provider.ruSize === 0) {
      return false
    }

    // Check if position is valid and has enough space
    if (!canPlaceProvider(rackId, position, provider.ruSize)) {
      return false
    }

    // Update provider with rack placement
    return placeProviderInRack(providerId, rackId, position)
  }

  const removeProviderFromRack = (providerId) => {
    const { removeProviderFromRack: removeProvider } = useResourceProviders()
    return removeProvider(providerId)
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
    resetConfiguration,
    addRack,
    deleteRack,
    reorderRacks,
    canPlaceProvider,
    addProviderToRack,
    removeProviderFromRack
  }
}