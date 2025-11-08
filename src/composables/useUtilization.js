import { computed } from 'vue'
import { useRackConfig } from './useRackConfig'
import { calculateHeatLoad } from '../utils/calculations'

export function useUtilization() {
  const { config } = useRackConfig()

  // Calculate total power used across all racks and unracked devices
  const powerUsed = computed(() => {
    let total = 0

    // Add power from devices in racks
    for (const rack of config.value.racks) {
      for (const device of rack.devices) {
        total += device.powerDraw || 0
      }
    }

    // Add power from unracked devices
    if (config.value.unrackedDevices) {
      for (const device of config.value.unrackedDevices) {
        total += device.powerDraw || 0
      }
    }

    return Math.round(total)
  })

  const powerCapacity = computed(() => {
    return config.value.settings.totalPowerCapacity || 0
  })

  const powerPercentage = computed(() => {
    if (powerCapacity.value === 0) return 0
    return Math.min(100, Math.round((powerUsed.value / powerCapacity.value) * 100))
  })

  // Calculate HVAC load (1:1 with power draw, converted to BTU/hr)
  const hvacLoad = computed(() => {
    // Heat load equals power consumption converted to BTU/hr
    return Math.round(calculateHeatLoad(powerUsed.value))
  })

  const hvacCapacity = computed(() => {
    return config.value.settings.hvacCapacity || 0
  })

  const hvacPercentage = computed(() => {
    if (hvacCapacity.value === 0) return 0
    return Math.min(100, Math.round((hvacLoad.value / hvacCapacity.value) * 100))
  })

  // Calculate RU utilization across all racks
  const ruUsed = computed(() => {
    let total = 0
    for (const rack of config.value.racks) {
      for (const device of rack.devices) {
        total += device.ruSize || 0
      }
    }
    return total
  })

  const ruCapacity = computed(() => {
    const ruPerRack = config.value.settings.ruPerRack || 42
    const rackCount = config.value.racks.length
    return ruPerRack * rackCount
  })

  const ruPercentage = computed(() => {
    if (ruCapacity.value === 0) return 0
    return Math.min(100, Math.round((ruUsed.value / ruCapacity.value) * 100))
  })

  const isOverCapacity = computed(() => {
    return powerPercentage.value > 100 || hvacPercentage.value > 100
  })

  return {
    powerUsed,
    powerCapacity,
    powerPercentage,
    hvacLoad,
    hvacCapacity,
    hvacPercentage,
    ruUsed,
    ruCapacity,
    ruPercentage,
    isOverCapacity
  }
}