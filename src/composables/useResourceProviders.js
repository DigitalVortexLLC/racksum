import { ref, computed, onMounted, onUnmounted } from 'vue'
import { logError, logWarn, logInfo, logDebug } from '../utils/logger'

// Resource provider types
export const PROVIDER_TYPES = {
  POWER: 'power',
  COOLING: 'cooling',
  NETWORK: 'network'
}

const resourceProviders = ref([])

export function useResourceProviders() {
  const loadProviders = () => {
    const saved = localStorage.getItem('racker-resource-providers')
    if (saved) {
      try {
        resourceProviders.value = JSON.parse(saved)
      } catch (err) {
        logError('Error loading resource providers', err)
        resourceProviders.value = []
      }
    }
  }

  const saveProviders = () => {
    localStorage.setItem('racker-resource-providers', JSON.stringify(resourceProviders.value))
  }

  const handleProvidersUpdated = () => {
    loadProviders()
  }

  onMounted(() => {
    if (resourceProviders.value.length === 0) {
      loadProviders()
    }
    window.addEventListener('resource-providers-updated', handleProvidersUpdated)
  })

  onUnmounted(() => {
    window.removeEventListener('resource-providers-updated', handleProvidersUpdated)
  })

  const addProvider = (provider) => {
    const newProvider = {
      id: `provider-${Date.now()}`,
      name: provider.name,
      type: provider.type,
      powerCapacity: provider.powerCapacity || 0,
      powerPortsCapacity: provider.powerPortsCapacity || 0, // Number of PDU power ports
      coolingCapacity: provider.coolingCapacity || 0, // BTU/hr
      networkCapacity: provider.networkCapacity || 0, // Gbps
      description: provider.description || '',
      location: provider.location || '',
      // RU space consumption properties (optional)
      ruSize: provider.ruSize || 0, // How many RUs this provider occupies (0 = not racked)
      rackId: provider.rackId || null, // Which rack it's placed in (null = not racked)
      position: provider.position || null, // Starting RU position in rack (null = not racked)
      // Placement tracking - templates vs placed instances
      isPlaced: provider.isPlaced || false, // false = template in library, true = placed instance
      custom: true,
      createdAt: new Date().toISOString()
    }

    resourceProviders.value.push(newProvider)
    saveProviders()
    window.dispatchEvent(new CustomEvent('resource-providers-updated'))
    return newProvider
  }

  const updateProvider = (providerId, updates) => {
    const index = resourceProviders.value.findIndex(p => p.id === providerId)
    if (index !== -1) {
      resourceProviders.value[index] = {
        ...resourceProviders.value[index],
        ...updates,
        updatedAt: new Date().toISOString()
      }
      saveProviders()
      window.dispatchEvent(new CustomEvent('resource-providers-updated'))
      return true
    }
    return false
  }

  const deleteProvider = (providerId) => {
    resourceProviders.value = resourceProviders.value.filter(p => p.id !== providerId)
    saveProviders()
    window.dispatchEvent(new CustomEvent('resource-providers-updated'))
  }

  const getProviderById = (providerId) => {
    return resourceProviders.value.find(p => p.id === providerId)
  }

  // Computed totals - ONLY count placed providers (not templates)
  const totalPowerCapacity = computed(() => {
    return resourceProviders.value
      .filter(p => p.isPlaced === true)
      .reduce((sum, provider) => {
        return sum + (provider.powerCapacity || 0)
      }, 0)
  })

  const totalPowerPortsCapacity = computed(() => {
    return resourceProviders.value
      .filter(p => p.isPlaced === true)
      .reduce((sum, provider) => {
        return sum + (provider.powerPortsCapacity || 0)
      }, 0)
  })

  const totalCoolingCapacity = computed(() => {
    return resourceProviders.value
      .filter(p => p.isPlaced === true)
      .reduce((sum, provider) => {
        return sum + (provider.coolingCapacity || 0)
      }, 0)
  })

  const totalNetworkCapacity = computed(() => {
    return resourceProviders.value
      .filter(p => p.isPlaced === true)
      .reduce((sum, provider) => {
        return sum + (provider.networkCapacity || 0)
      }, 0)
  })

  // Get providers by type
  const getPowerProviders = computed(() => {
    return resourceProviders.value.filter(p => p.type === PROVIDER_TYPES.POWER)
  })

  const getCoolingProviders = computed(() => {
    return resourceProviders.value.filter(p => p.type === PROVIDER_TYPES.COOLING)
  })

  const getNetworkProviders = computed(() => {
    return resourceProviders.value.filter(p => p.type === PROVIDER_TYPES.NETWORK)
  })

  // Get template providers (library items)
  const getTemplateProviders = computed(() => {
    return resourceProviders.value.filter(p => p.isPlaced === false)
  })

  // Get placed providers (actual instances)
  const getPlacedProviders = computed(() => {
    return resourceProviders.value.filter(p => p.isPlaced === true)
  })

  // Get racked vs unracked providers (only placed ones)
  const getRackedProviders = computed(() => {
    return resourceProviders.value.filter(p => p.isPlaced === true && p.rackId && p.position && p.ruSize > 0)
  })

  const getUnrackedProviders = computed(() => {
    return resourceProviders.value.filter(p => p.isPlaced === true && (!p.rackId || !p.position || p.ruSize === 0))
  })

  // Get providers for a specific rack
  const getProvidersForRack = (rackId) => {
    return resourceProviders.value.filter(p => p.rackId === rackId && p.position && p.ruSize > 0)
  }

  // Create instance from template (when dragging from library)
  const createInstanceFromTemplate = (templateProvider, options = {}) => {
    const instance = {
      ...templateProvider,
      id: `provider-instance-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      isPlaced: true,
      rackId: options.rackId || null,
      position: options.position || null,
      createdAt: new Date().toISOString()
    }

    resourceProviders.value.push(instance)
    saveProviders()
    window.dispatchEvent(new CustomEvent('resource-providers-updated'))
    return instance
  }

  // Place provider in rack
  const placeProviderInRack = (providerId, rackId, position) => {
    const provider = getProviderById(providerId)
    if (!provider || !provider.ruSize || provider.ruSize === 0) {
      return false
    }

    return updateProvider(providerId, {
      rackId,
      position,
      isPlaced: true
    })
  }

  // Remove provider from rack
  const removeProviderFromRack = (providerId) => {
    return updateProvider(providerId, {
      rackId: null,
      position: null
    })
  }

  // Calculate total RU used by providers
  const totalProviderRU = computed(() => {
    return resourceProviders.value.reduce((sum, provider) => {
      return sum + (provider.ruSize || 0)
    }, 0)
  })

  // Calculate RU used by racked providers
  const rackedProviderRU = computed(() => {
    return getRackedProviders.value.reduce((sum, provider) => {
      return sum + (provider.ruSize || 0)
    }, 0)
  })

  // Export/Import functionality
  const exportProviders = () => {
    return {
      providers: resourceProviders.value,
      exportDate: new Date().toISOString(),
      version: '1.0'
    }
  }

  const importProviders = (data, mode = 'merge') => {
    if (!data.providers || !Array.isArray(data.providers)) {
      throw new Error('Invalid import data: missing or invalid "providers" array')
    }

    // Validate required fields
    for (const provider of data.providers) {
      if (!provider.name || !provider.type) {
        throw new Error('Invalid provider: missing required fields (name, type)')
      }
    }

    if (mode === 'replace') {
      resourceProviders.value = data.providers
    } else {
      // Merge mode: add new providers
      const existingIds = new Set(resourceProviders.value.map(p => p.id))
      let added = 0

      for (const provider of data.providers) {
        if (!existingIds.has(provider.id)) {
          resourceProviders.value.push(provider)
          added++
        }
      }

      return added
    }

    saveProviders()
    window.dispatchEvent(new CustomEvent('resource-providers-updated'))
  }

  return {
    resourceProviders,
    totalPowerCapacity,
    totalPowerPortsCapacity,
    totalCoolingCapacity,
    totalNetworkCapacity,
    getPowerProviders,
    getCoolingProviders,
    getNetworkProviders,
    getTemplateProviders,
    getPlacedProviders,
    getRackedProviders,
    getUnrackedProviders,
    getProvidersForRack,
    totalProviderRU,
    rackedProviderRU,
    addProvider,
    updateProvider,
    deleteProvider,
    getProviderById,
    createInstanceFromTemplate,
    placeProviderInRack,
    removeProviderFromRack,
    exportProviders,
    importProviders,
    loadProviders
  }
}
