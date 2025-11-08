import { ref } from 'vue'
import { useRackConfig } from './useRackConfig'
import { useToast } from './useToast'

const draggedDevice = ref(null)
const cannotFitAnimation = ref(false)

export function useDragDrop() {
  const { addDeviceToRack, canPlaceDevice } = useRackConfig()
  const { showSuccess, showError } = useToast()

  const startDrag = (event, device) => {
    draggedDevice.value = device
    event.dataTransfer.effectAllowed = 'copy'
    event.dataTransfer.setData('application/json', JSON.stringify(device))
  }

  const handleDrop = (event, rackId, position) => {
    event.preventDefault()

    if (!draggedDevice.value) {
      // Try to get from dataTransfer
      try {
        const data = event.dataTransfer.getData('application/json')
        if (data) {
          draggedDevice.value = JSON.parse(data)
        }
      } catch (error) {
        console.error('Failed to parse dropped device:', error)
        return
      }
    }

    if (!draggedDevice.value) return

    const device = draggedDevice.value

    // Check if device can be placed
    if (!canPlaceDevice(rackId, position, device.ruSize)) {
      // Trigger wiggle animation
      triggerCannotFitAnimation()
      showError('Cannot place device', 'Not enough space at this position')
      draggedDevice.value = null
      return
    }

    // Add device to rack
    const success = addDeviceToRack(rackId, device, position)

    if (!success) {
      triggerCannotFitAnimation()
      showError('Cannot place device', 'Failed to add device to rack')
    } else {
      showSuccess('Device added', `${device.customName || device.name} placed at position ${position}`)
    }

    draggedDevice.value = null
  }

  const triggerCannotFitAnimation = () => {
    cannotFitAnimation.value = true
    setTimeout(() => {
      cannotFitAnimation.value = false
    }, 500)
  }

  const canDrop = (rackId, position, ruSize) => {
    return canPlaceDevice(rackId, position, ruSize)
  }

  return {
    draggedDevice,
    cannotFitAnimation,
    startDrag,
    handleDrop,
    canDrop,
    triggerCannotFitAnimation
  }
}