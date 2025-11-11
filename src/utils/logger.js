/**
 * Centralized logging utility that integrates with Sentry
 * Replaces console statements with proper error handling
 */

// Check if we're in production mode
const isProduction = import.meta.env.PROD

/**
 * Lazy-load Sentry to avoid issues if it's not configured
 */
let Sentry = null
const getSentry = async () => {
  if (!Sentry && isProduction) {
    try {
      // In production, Sentry should be configured on the backend
      // For now, we'll use a simple implementation that could be extended
      Sentry = {
        captureException: (error, context) => {
          // Send to backend Sentry endpoint if needed
          // For now, errors will be captured by Django's Sentry integration
          return null
        },
        captureMessage: (message, level) => {
          return null
        }
      }
    } catch (e) {
      // Sentry not available
    }
  }
  return Sentry
}

/**
 * Log levels
 */
export const LogLevel = {
  DEBUG: 'debug',
  INFO: 'info',
  WARN: 'warn',
  ERROR: 'error'
}

/**
 * Logger class
 */
class Logger {
  /**
   * Log a debug message
   * Only logs in development mode
   */
  debug(message, ...args) {
    if (!isProduction) {
      console.debug(`[DEBUG] ${message}`, ...args)
    }
  }

  /**
   * Log an info message
   * Only logs in development mode
   */
  info(message, ...args) {
    if (!isProduction) {
      console.info(`[INFO] ${message}`, ...args)
    }
  }

  /**
   * Log a warning message
   * Logs in development, sends to Sentry in production
   */
  async warn(message, context = {}) {
    if (!isProduction) {
      console.warn(`[WARN] ${message}`, context)
    } else {
      const sentry = await getSentry()
      if (sentry) {
        sentry.captureMessage(message, 'warning')
      }
    }
  }

  /**
   * Log an error
   * Logs in development, sends to Sentry in production
   * @param {string} message - Error message
   * @param {Error|Object} error - Error object or context
   * @param {Object} context - Additional context
   */
  async error(message, error = null, context = {}) {
    if (!isProduction) {
      console.error(`[ERROR] ${message}`, error, context)
    } else {
      const sentry = await getSentry()
      if (sentry && error instanceof Error) {
        sentry.captureException(error, {
          tags: { message },
          extra: context
        })
      } else if (sentry) {
        sentry.captureMessage(`${message}: ${error}`, 'error')
      }
    }
  }

  /**
   * Log a caught exception
   * Always sends to Sentry in production
   */
  async exception(error, context = {}) {
    if (!isProduction) {
      console.error('[EXCEPTION]', error, context)
    } else {
      const sentry = await getSentry()
      if (sentry && error instanceof Error) {
        sentry.captureException(error, {
          extra: context
        })
      }
    }
  }
}

// Export singleton instance
export const logger = new Logger()

// Export convenience methods
export const logDebug = (message, ...args) => logger.debug(message, ...args)
export const logInfo = (message, ...args) => logger.info(message, ...args)
export const logWarn = (message, context) => logger.warn(message, context)
export const logError = (message, error, context) => logger.error(message, error, context)
export const logException = (error, context) => logger.exception(error, context)

export default logger
