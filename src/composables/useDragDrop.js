import { ref } from 'vue'
import { useRackConfig } from './useRackConfig'
import { useResourceProviders } from './useResourceProviders'
import { useToast } from './useToast'
import { logError, logWarn, logInfo, logDebug } from '../utils/logger'

const draggedDevice = ref(null)
const draggedProvider = ref(null)
const dragSource = ref(null) // { type: 'library' | 'unracked' | 'rack' | 'provider-library', rackId?, position? }
const cannotFitAnimation = ref(false)

export function useDragDrop() {
  const { addDeviceToRack, canPlaceDevice, removeDeviceFromRack } = useRackConfig()
  const { createInstanceFromTemplate, updateProvider, deleteProvider } = useResourceProviders()
  const { showSuccess, showError } = useToast()

  const startDrag = (event, item, source = { type: 'library' }) => {
    // Determine if dragging a device or provider
    if (source.type === 'provider-library') {
      draggedProvider.value = item
      draggedDevice.value = null
      event.dataTransfer.effectAllowed = 'copy'
      event.dataTransfer.setData('application/json', JSON.stringify({ provider: item, source }))
    } else {
      draggedDevice.value = item
      draggedProvider.value = null
      event.dataTransfer.effectAllowed = 'move'
      event.dataTransfer.setData('application/json', JSON.stringify({ device: item, source }))
    }
    dragSource.value = source
  }

  const handleDrop = (event, rackId, position) => {
    event.preventDefault()

    let device = draggedDevice.value
    let provider = draggedProvider.value
    let source = dragSource.value

    // Try to get from dataTransfer if not set
    if (!device && !provider) {
      try {
        const data = event.dataTransfer.getData('application/json')
        if (data) {
          const parsed = JSON.parse(data)
          if (parsed.provider) {
            provider = parsed.provider
            draggedProvider.value = provider
          } else if (parsed.device) {
            device = parsed.device
            draggedDevice.value = device
          }
          source = parsed.source || { type: 'library' }
          dragSource.value = source
        }
      } catch (error) {
        logError('Failed to parse dropped item', error)
        return
      }
    }

    // Handle provider drop
    if (provider) {
      // Check if provider needs rack space
      if (provider.ruSize > 0) {
        // Provider needs rack space - validate placement
        if (!canPlaceDevice(rackId, position, provider.ruSize)) {
          triggerCannotFitAnimation()
          showError('Cannot place provider', 'Not enough space at this position')
          draggedProvider.value = null
          dragSource.value = null
          return
        }

        // Create instance from template
        const instance = createInstanceFromTemplate(provider, { rackId, position })
        if (instance) {
          showSuccess('Provider placed', `${provider.name} placed at position ${position}`)
        }
      } else {
        // Provider is virtual (ruSize = 0) - cannot go in rack
        showError('Cannot place provider', 'This provider does not use rack space. Drag it to unracked devices instead.')
      }

      draggedProvider.value = null
      dragSource.value = null
      return
    }

    // Handle device drop
    if (!device) return

    // Check if we're dropping in the same location
    if (source?.type === 'rack' && source.rackId === rackId && source.position === position) {
      draggedDevice.value = null
      dragSource.value = null
      return
    }

    // Check if device can be placed (excluding the device itself if moving from rack)
    if (!canPlaceDevice(rackId, position, device.ruSize, device.instanceId)) {
      // Trigger wiggle animation
      triggerCannotFitAnimation()
      showError('Cannot place device', 'Not enough space at this position')
      draggedDevice.value = null
      dragSource.value = null
      return
    }

    // If moving from a rack, remove it from the old position first
    if (source?.type === 'rack' && device.instanceId) {
      removeDeviceFromRack(source.rackId, device.instanceId)
    }

    // Add device to rack
    const success = addDeviceToRack(rackId, device, position)

    if (!success) {
      triggerCannotFitAnimation()
      showError('Cannot place device', 'Failed to add device to rack')
    } else {
      const action = source?.type === 'rack' ? 'moved to' : 'placed at'
      showSuccess('Device ' + (source?.type === 'rack' ? 'moved' : 'added'), `${device.customName || device.name} ${action} position ${position}`)
    }

    draggedDevice.value = null
    dragSource.value = null
  }

  const triggerCannotFitAnimation = () => {
    cannotFitAnimation.value = true
    setTimeout(() => {
      cannotFitAnimation.value = false
    }, 500)
  }

  const handleDropToUnracked = (event) => {
    event.preventDefault()

    let device = draggedDevice.value
    let provider = draggedProvider.value
    let source = dragSource.value

    // Try to get from dataTransfer if not set
    if (!device && !provider) {
      try {
        const data = event.dataTransfer.getData('application/json')
        if (data) {
          const parsed = JSON.parse(data)
          if (parsed.provider) {
            provider = parsed.provider
            draggedProvider.value = provider
          } else if (parsed.device) {
            device = parsed.device
            draggedDevice.value = device
          }
          source = parsed.source || { type: 'library' }
          dragSource.value = source
        }
      } catch (error) {
        logError('Failed to parse dropped item', error)
        return
      }
    }

    // Handle provider drop to unracked
    if (provider) {
      // Create instance from template (unracked)
      const instance = createInstanceFromTemplate(provider, {})
      if (instance) {
        showSuccess('Provider added', `${provider.name} added to unracked providers`)
      }

      draggedProvider.value = null
      dragSource.value = null
      return
    }

    // Handle device drop to unracked
    if (!device) return

    // Only allow moving from rack to unracked (not from library or already unracked)
    if (source?.type === 'rack' && device.instanceId) {
      const { addUnrackedDevice, removeDeviceFromRack } = useRackConfig()

      // Remove from rack
      removeDeviceFromRack(source.rackId, device.instanceId)

      // Add to unracked
      addUnrackedDevice(device)

      showSuccess('Device unracked', `${device.customName || device.name} moved to unracked devices`)
    }

    draggedDevice.value = null
    dragSource.value = null
  }

  const canDrop = (rackId, position, ruSize) => {
    return canPlaceDevice(rackId, position, ruSize)
  }

  return {
    draggedDevice,
    draggedProvider,
    dragSource,
    cannotFitAnimation,
    startDrag,
    handleDrop,
    handleDropToUnracked,
    canDrop,
    triggerCannotFitAnimation
  }
}