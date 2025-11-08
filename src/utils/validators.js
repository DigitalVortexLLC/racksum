/**
 * Validate rack configuration JSON structure
 *
 * @param {Object} config - Configuration object to validate
 * @returns {Object} { valid: boolean, errors: string[] }
 */
export function validateRackConfig(config) {
  const errors = []

  // Check required top-level properties
  if (!config) {
    errors.push('Configuration is null or undefined')
    return { valid: false, errors }
  }

  if (typeof config !== 'object') {
    errors.push('Configuration must be an object')
    return { valid: false, errors }
  }

  // Validate settings
  if (!config.settings) {
    errors.push('Missing settings object')
  } else {
    if (typeof config.settings.totalPowerCapacity !== 'number') {
      errors.push('settings.totalPowerCapacity must be a number')
    }
    if (typeof config.settings.hvacCapacity !== 'number') {
      errors.push('settings.hvacCapacity must be a number')
    }
    if (typeof config.settings.ruPerRack !== 'number') {
      errors.push('settings.ruPerRack must be a number')
    }
    if (config.settings.ruPerRack < 1 || config.settings.ruPerRack > 52) {
      errors.push('settings.ruPerRack must be between 1 and 52')
    }
  }

  // Validate racks array
  if (!Array.isArray(config.racks)) {
    errors.push('racks must be an array')
  } else {
    config.racks.forEach((rack, index) => {
      if (!rack.id) {
        errors.push(`Rack at index ${index} missing id`)
      }
      if (!rack.name) {
        errors.push(`Rack at index ${index} missing name`)
      }
      if (!Array.isArray(rack.devices)) {
        errors.push(`Rack at index ${index} devices must be an array`)
      } else {
        rack.devices.forEach((device, deviceIndex) => {
          if (!device.deviceId && !device.id) {
            errors.push(`Device at rack ${index}, position ${deviceIndex} missing deviceId`)
          }
          if (typeof device.position !== 'number') {
            errors.push(`Device at rack ${index}, position ${deviceIndex} missing or invalid position`)
          }
          if (typeof device.ruSize !== 'number') {
            errors.push(`Device at rack ${index}, position ${deviceIndex} missing or invalid ruSize`)
          }
        })
      }
    })
  }

  return {
    valid: errors.length === 0,
    errors
  }
}

/**
 * Validate device object
 *
 * @param {Object} device - Device object to validate
 * @returns {Object} { valid: boolean, errors: string[] }
 */
export function validateDevice(device) {
  const errors = []

  if (!device) {
    errors.push('Device is null or undefined')
    return { valid: false, errors }
  }

  const requiredFields = ['id', 'name', 'category', 'ruSize', 'powerDraw', 'color']
  requiredFields.forEach(field => {
    if (!(field in device)) {
      errors.push(`Missing required field: ${field}`)
    }
  })

  if (typeof device.ruSize !== 'number' || device.ruSize < 0) {
    errors.push('ruSize must be a non-negative number')
  }

  if (typeof device.powerDraw !== 'number' || device.powerDraw < 0) {
    errors.push('powerDraw must be a non-negative number')
  }

  return {
    valid: errors.length === 0,
    errors
  }
}