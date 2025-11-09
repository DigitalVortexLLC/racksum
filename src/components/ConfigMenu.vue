<template>
  <div
    class="fixed inset-0 flex items-center justify-center z-50 transition-opacity duration-200"
    style="background-color: rgba(0, 0, 0, 0.3); backdrop-filter: blur(4px);"
    @click.self="$emit('close')"
  >
    <div class="rounded-xl shadow-2xl w-full max-w-md transform transition-all duration-200 scale-100 hover:scale-[1.01]" style="background-color: var(--bg-primary);">
      <div class="flex items-center justify-between mb-6 p-6 rounded-t-xl" style="background-color: var(--color-primary);">
        <h2 class="text-2xl font-bold" style="color: #0c0c0d;">Infrastructure Settings</h2>
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

      <div class="px-6 pb-6">
        <p class="mb-4 text-sm" style="color: var(--text-secondary);">
          Configure infrastructure-level settings. Use the + button to add racks.
        </p>

        <!-- RU per Rack -->
        <div class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            RU per Rack
          </label>
        <input
          v-model.number="localSettings.ruPerRack"
          type="number"
          min="1"
          max="52"
          class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
          style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
          @focus="$event.target.style.borderColor = 'var(--color-primary)'; $event.target.style.boxShadow = '0 0 0 2px rgba(132, 204, 22, 0.2)'"
            @blur="$event.target.style.borderColor = 'var(--border-color)'; $event.target.style.boxShadow = 'none'"
          />
        </div>

        <!-- Resource Providers Note -->
        <div class="mb-6 p-4 rounded border" style="background-color: rgba(74, 144, 226, 0.1); border-color: var(--color-primary);">
          <p class="text-sm" style="color: var(--text-primary);">
            <strong>💡 Power & Cooling Capacity</strong>
          </p>
          <p class="text-xs mt-2" style="color: var(--text-secondary);">
            Capacity is now managed through <strong>Resource Providers</strong>.
            Open the Device Manager and go to the "Resource Providers" tab to add PDUs, HVAC units, and other infrastructure that provides capacity to your site.
          </p>
        </div>

        <!-- Buttons -->
        <div class="flex gap-2">
        <button
          @click="saveSettings"
          class="flex-1 px-4 py-2 text-white rounded transition-colors"
          style="background-color: var(--color-primary);"
          @mouseover="$event.target.style.backgroundColor = 'var(--color-primary-dark)'"
          @mouseout="$event.target.style.backgroundColor = 'var(--color-primary)'"
        >
          Save
        </button>
        <button
          @click="$emit('close')"
          class="flex-1 px-4 py-2 text-white rounded transition-colors"
          style="background-color: var(--color-primary-light); color: var(--color-primary-dark);"
          @mouseover="$event.target.style.opacity = '0.8'"
          @mouseout="$event.target.style.opacity = '1'"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRackConfig } from '../composables/useRackConfig'
import { useToast } from '../composables/useToast'

const emit = defineEmits(['close'])

const { config, updateSettings } = useRackConfig()
const { showSuccess } = useToast()

const localSettings = ref({
  ruPerRack: 42
})

onMounted(() => {
  localSettings.value = {
    ruPerRack: config.value.settings.ruPerRack
  }
})

const saveSettings = () => {
  updateSettings({
    ruPerRack: localSettings.value.ruPerRack
  })

  showSuccess('Settings saved', 'Infrastructure settings have been updated successfully')
  emit('close')
}
</script>
