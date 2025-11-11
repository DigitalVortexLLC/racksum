import { ref } from 'vue'
import { useRackConfig } from './useRackConfig'
import { useToast } from './useToast'
import { logError, logWarn, logInfo, logDebug } from '../utils/logger'

const draggedDevice = ref(null)
const dragSource = ref(null) // { type: 'library' | 'unracked' | 'rack', rackId?, position? }
const cannotFitAnimation = ref(false)

export function useDragDrop() {
  const { addDeviceToRack, canPlaceDevice, removeDeviceFromRack } = useRackConfig()
  const { showSuccess, showError } = useToast()

  const startDrag = (event, device, source = { type: 'library' }) => {
    draggedDevice.value = device
    dragSource.value = source
    event.dataTransfer.effectAllowed = 'move'
    event.dataTransfer.setData('application/json', JSON.stringify({ device, source }))
  }

  const handleDrop = (event, rackId, position) => {
    event.preventDefault()

    let device = draggedDevice.value
    let source = dragSource.value

    if (!device) {
      // Try to get from dataTransfer
      try {
        const data = event.dataTransfer.getData('application/json')
        if (data) {
          const parsed = JSON.parse(data)
          device = parsed.device || parsed
          source = parsed.source || { type: 'library' }
          draggedDevice.value = device
          dragSource.value = source
        }
      } catch (error) {
        logError('Failed to parse dropped device', error)
        return
      }
    }

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
    let source = dragSource.value

    if (!device) {
      // Try to get from dataTransfer
      try {
        const data = event.dataTransfer.getData('application/json')
        if (data) {
          const parsed = JSON.parse(data)
          device = parsed.device || parsed
          source = parsed.source || { type: 'library' }
          draggedDevice.value = device
          dragSource.value = source
        }
      } catch (error) {
        logError('Failed to parse dropped device', error)
        return
      }
    }

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
    dragSource,
    cannotFitAnimation,
    startDrag,
    handleDrop,
    handleDropToUnracked,
    canDrop,
    triggerCannotFitAnimation
  }
}