/**
 * Calculate heat load in BTU/hr from power consumption in watts
 * Formula: 1 Watt = 3.41 BTU/hr
 *
 * @param {number} watts - Power consumption in watts
 * @returns {number} Heat load in BTU/hr
 */
export function calculateHeatLoad(watts) {
  const BTU_PER_WATT = 3.41
  return watts * BTU_PER_WATT
}

/**
 * Convert BTU/hr to watts
 *
 * @param {number} btu - Heat in BTU/hr
 * @returns {number} Equivalent watts
 */
export function btuToWatts(btu) {
  const BTU_PER_WATT = 3.41
  return btu / BTU_PER_WATT
}

/**
 * Convert watts to kilowatts
 *
 * @param {number} watts - Power in watts
 * @returns {number} Power in kilowatts
 */
export function wattsToKilowatts(watts) {
  return watts / 1000
}

/**
 * Calculate utilization percentage
 *
 * @param {number} used - Amount used
 * @param {number} total - Total capacity
 * @returns {number} Percentage (0-100)
 */
export function calculateUtilization(used, total) {
  if (total === 0) return 0
  return Math.min(100, Math.round((used / total) * 100))
}

/**
 * Get utilization status color
 *
 * @param {number} percentage - Utilization percentage
 * @returns {string} Color indicator ('green', 'yellow', 'red')
 */
export function getUtilizationStatus(percentage) {
  if (percentage < 70) return 'green'
  if (percentage < 90) return 'yellow'
  return 'red'
}

/**
 * Convert Refrigeration Tons to BTU/hr
 * Formula: 1 Refrigeration Ton = 12,000 BTU/hr
 *
 * @param {number} tons - Refrigeration capacity in tons
 * @returns {number} Capacity in BTU/hr
 */
export function tonsToBtu(tons) {
  const BTU_PER_TON = 12000
  return tons * BTU_PER_TON
}

/**
 * Convert BTU/hr to Refrigeration Tons
 *
 * @param {number} btu - Heat in BTU/hr
 * @returns {number} Refrigeration Tons
 */
export function btuToTons(btu) {
  const BTU_PER_TON = 12000
  return btu / BTU_PER_TON
}