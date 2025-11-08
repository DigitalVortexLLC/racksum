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

  return {
    showSuccess,
    showError,
    showInfo,
    showWarn
  }
}