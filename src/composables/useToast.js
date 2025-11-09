import { useToast as usePrimeToast } from 'primevue/usetoast'

export function useToast() {
  const toast = usePrimeToast()

  const showSuccess = (message, detail = '') => {
    toast.add({
      severity: 'success',
      summary: message,
      detail,
      life: 3000
    })
  }

  const showError = (message, detail = '') => {
    toast.add({
      severity: 'error',
      summary: message,
      detail,
      life: 5000
    })
  }

  const showInfo = (message, detail = '') => {
    toast.add({
      severity: 'info',
      summary: message,
      detail,
      life: 3000
    })
  }

  const showWarn = (message, detail = '') => {
    toast.add({
      severity: 'warn',
      summary: message,
      detail,
      life: 4000
    })
  }

  // Generic showToast function that maps severity to specific functions
  const showToast = (severity, message, detail = '') => {
    const severityMap = {
      'success': showSuccess,
      'error': showError,
      'info': showInfo,
      'warn': showWarn,
      'warning': showWarn
    }

    const toastFn = severityMap[severity] || showInfo
    toastFn(message, detail)
  }

  return {
    showSuccess,
    showError,
    showInfo,
    showWarn,
    showToast
  }
}