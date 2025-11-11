import { createApp } from 'vue'
import './assets/main.css'
import App from './App.vue'
import { logError } from './utils/logger'

const app = createApp(App)

// Global error handler to catch component errors
app.config.errorHandler = (err, instance, info) => {
  // Log error to our logging service
  logError('Vue component error', err, {
    componentName: instance?.$options?.name || 'Unknown',
    errorInfo: info,
    componentStack: instance?.$options?.__file
  })

  // In development, also log to console for debugging
  if (import.meta.env.DEV) {
    console.error('Vue error:', err)
    console.error('Component:', instance)
    console.error('Error info:', info)
  }
}

// Catch warnings in development
if (import.meta.env.DEV) {
  app.config.warnHandler = (msg, instance, trace) => {
    console.warn('Vue warning:', msg)
    console.warn('Component:', instance)
    console.warn('Trace:', trace)
  }
}

// Global handler for unhandled promise rejections
window.addEventListener('unhandledrejection', event => {
  logError('Unhandled promise rejection', event.reason, {
    promise: event.promise
  })

  if (import.meta.env.DEV) {
    console.error('Unhandled promise rejection:', event.reason)
  }
})

// Global handler for general JavaScript errors
window.addEventListener('error', event => {
  logError('Uncaught error', event.error || new Error(event.message), {
    filename: event.filename,
    lineno: event.lineno,
    colno: event.colno
  })

  if (import.meta.env.DEV) {
    console.error('Uncaught error:', event.error || event.message)
  }
})

app.mount('#app')