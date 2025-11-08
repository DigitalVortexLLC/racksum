<template>
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 backdrop-blur-sm transition-opacity duration-200"
    @click.self="$emit('close')"
  >
    <div class="rounded-xl shadow-2xl w-full max-w-2xl transform transition-all duration-200" style="background-color: var(--bg-primary);">
      <div class="flex items-center justify-between mb-6 p-6 rounded-t-xl" style="background-color: var(--color-primary);">
        <h2 class="text-2xl font-bold" style="color: #0c0c0d;">Import / Export Configuration</h2>
        <button
          @click="$emit('close')"
          class="transition-colors"
          style="color: rgba(12, 12, 13, 0.7);"
          @mouseover="$event.target.style.color = '#0c0c0d'"
          @mouseout="$event.target.style.color = 'rgba(12, 12, 13, 0.7)'"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="px-6">

      <!-- Tabs -->
      <div class="flex mb-4" style="border-bottom: 1px solid var(--border-color);">
        <button
          @click="activeTab = 'export'"
          class="px-4 py-2 border-b-2 border-transparent font-medium transition-colors"
          :style="{
            borderColor: activeTab === 'export' ? 'var(--color-primary)' : 'transparent',
            color: activeTab === 'export' ? 'var(--color-primary)' : 'var(--text-primary)'
          }"
        >
          Export
        </button>
        <button
          @click="activeTab = 'import'"
          class="px-4 py-2 border-b-2 border-transparent font-medium transition-colors"
          :style="{
            borderColor: activeTab === 'import' ? 'var(--color-primary)' : 'transparent',
            color: activeTab === 'import' ? 'var(--color-primary)' : 'var(--text-primary)'
          }"
        >
          Import
        </button>
      </div>

      <!-- Export Tab -->
      <div v-if="activeTab === 'export'" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            Configuration JSON
          </label>
          <textarea
            :value="exportJson"
            readonly
            class="w-full h-64 px-3 py-2 rounded font-mono text-xs focus:outline-none transition-colors"
            style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
            @focus="$event.target.style.borderColor = 'var(--color-primary)'; $event.target.style.boxShadow = '0 0 0 2px rgba(132, 204, 22, 0.2)'"
            @blur="$event.target.style.borderColor = 'var(--border-color)'; $event.target.style.boxShadow = 'none'"
          ></textarea>
        </div>
        <div class="flex gap-2">
          <button
            @click="copyToClipboard"
            class="px-4 py-2 text-white rounded transition-colors"
            style="background-color: var(--color-primary);"
            @mouseover="$event.target.style.backgroundColor = 'var(--color-primary-dark)'"
            @mouseout="$event.target.style.backgroundColor = 'var(--color-primary)'"
          >
            {{ copyButtonText }}
          </button>
          <button
            @click="downloadJson"
            class="px-4 py-2 text-white rounded transition-colors"
            style="background-color: var(--color-accent);"
            @mouseover="$event.target.style.opacity = '0.9'"
            @mouseout="$event.target.style.opacity = '1'"
          >
            Download File
          </button>
        </div>
      </div>

      <!-- Import Tab -->
      <div v-if="activeTab === 'import'" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            Paste Configuration JSON
          </label>
          <textarea
            v-model="importJson"
            placeholder="Paste your configuration JSON here..."
            class="w-full h-64 px-3 py-2 rounded font-mono text-xs focus:outline-none transition-colors"
            style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
            @focus="$event.target.style.borderColor = 'var(--color-primary)'; $event.target.style.boxShadow = '0 0 0 2px rgba(132, 204, 22, 0.2)'"
            @blur="$event.target.style.borderColor = 'var(--border-color)'; $event.target.style.boxShadow = 'none'"
          ></textarea>
        </div>
        <div class="flex gap-2">
          <button
            @click="loadFromJson"
            class="px-4 py-2 text-white rounded transition-colors"
            style="background-color: var(--color-primary);"
            @mouseover="$event.target.style.backgroundColor = 'var(--color-primary-dark)'"
            @mouseout="$event.target.style.backgroundColor = 'var(--color-primary)'"
          >
            Load Configuration
          </button>
          <label
            class="px-4 py-2 text-white rounded cursor-pointer transition-opacity"
            style="background-color: var(--color-accent);"
            @mouseover="$event.target.style.opacity = '0.9'"
            @mouseout="$event.target.style.opacity = '1'"
          >
            Upload File
            <input
              type="file"
              accept=".json"
              @change="handleFileUpload"
              class="hidden"
            />
          </label>
        </div>
        <div v-if="importError" class="text-red-600 text-sm">
          {{ importError }}
        </div>
        <div v-if="importSuccess" class="text-green-600 text-sm">
          Configuration loaded successfully!
        </div>
      </div>

        <!-- Close Button -->
        <div class="mt-6 flex justify-end pb-6">
          <button
            @click="$emit('close')"
            class="px-4 py-2 rounded transition-opacity"
            style="background-color: var(--color-primary-light); color: var(--color-primary-dark);"
            @mouseover="$event.target.style.opacity = '0.8'"
            @mouseout="$event.target.style.opacity = '1'"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRackConfig } from '../composables/useRackConfig'
import { useToast } from '../composables/useToast'

const emit = defineEmits(['close'])

const { config, loadConfiguration } = useRackConfig()
const { showSuccess, showError } = useToast()

const activeTab = ref('export')
const importJson = ref('')
const importError = ref('')
const importSuccess = ref(false)
const copyButtonText = ref('Copy to Clipboard')

const exportJson = computed(() => {
  return JSON.stringify(config.value, null, 2)
})

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(exportJson.value)
    copyButtonText.value = 'Copied!'
    showSuccess('Copied to clipboard', 'Configuration JSON copied successfully')
    setTimeout(() => {
      copyButtonText.value = 'Copy to Clipboard'
    }, 2000)
  } catch (error) {
    console.error('Failed to copy:', error)
    showError('Copy failed', 'Failed to copy configuration to clipboard')
  }
}

const downloadJson = () => {
  const blob = new Blob([exportJson.value], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `racksum-config-${Date.now()}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  showSuccess('Download started', 'Configuration file download initiated')
}

const loadFromJson = () => {
  importError.value = ''
  importSuccess.value = false

  try {
    const parsed = JSON.parse(importJson.value)
    loadConfiguration(parsed)
    importSuccess.value = true
    showSuccess('Configuration imported', 'Your configuration has been loaded successfully')
    setTimeout(() => {
      emit('close')
    }, 1500)
  } catch (error) {
    importError.value = 'Invalid JSON: ' + error.message
    showError('Import failed', error.message)
  }
}

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = (e) => {
    importJson.value = e.target.result
    loadFromJson()
  }
  reader.readAsText(file)
}
</script>