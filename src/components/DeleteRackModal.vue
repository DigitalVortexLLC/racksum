<template>
  <div
    class="fixed inset-0 flex items-center justify-center z-50 transition-opacity duration-200"
    style="background-color: rgba(0, 0, 0, 0.3); backdrop-filter: blur(4px);"
    @click.self="$emit('close')"
  >
    <div class="rounded-xl shadow-2xl w-full max-w-md transform transition-all duration-200 scale-100" style="background-color: var(--bg-primary);">
      <div class="flex items-center justify-between mb-4 p-6 rounded-t-xl" style="background-color: #ef4444;">
        <h2 class="text-2xl font-bold text-white">Delete Rack</h2>
        <button
          @click="$emit('close')"
          class="transition-colors text-white hover:text-gray-200"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="px-6 pb-6">
        <p class="mb-4" style="color: var(--text-primary);">
          Are you sure you want to delete <strong>{{ rack.name }}</strong>?
        </p>

        <div v-if="rack.devices.length > 0" class="mb-6 p-4 rounded" style="background-color: var(--bg-secondary);">
          <p class="mb-3 font-medium" style="color: var(--text-primary);">
            This rack contains {{ rack.devices.length }} device{{ rack.devices.length > 1 ? 's' : '' }}.
          </p>

          <div class="space-y-2">
            <label class="flex items-center cursor-pointer">
              <input
                type="radio"
                v-model="deleteOption"
                value="move"
                class="mr-3"
              />
              <span style="color: var(--text-primary);">Move devices to unracked pane</span>
            </label>

            <label class="flex items-center cursor-pointer">
              <input
                type="radio"
                v-model="deleteOption"
                value="delete"
                class="mr-3"
              />
              <span style="color: var(--text-primary);">Delete all devices with rack</span>
            </label>
          </div>
        </div>

        <div v-else class="mb-6 p-4 rounded" style="background-color: var(--bg-secondary);">
          <p style="color: var(--text-secondary);">This rack is empty.</p>
        </div>

        <!-- Buttons -->
        <div class="flex gap-2">
          <button
            @click="$emit('close')"
            class="flex-1 px-4 py-2 rounded transition-colors"
            style="background-color: var(--bg-secondary); color: var(--text-primary);"
            @mouseover="$event.target.style.opacity = '0.8'"
            @mouseout="$event.target.style.opacity = '1'"
          >
            Cancel
          </button>
          <button
            @click="confirmDelete"
            class="flex-1 px-4 py-2 text-white rounded transition-colors"
            style="background-color: #ef4444;"
            @mouseover="$event.target.style.backgroundColor = '#dc2626'"
            @mouseout="$event.target.style.backgroundColor = '#ef4444'"
          >
            Delete Rack
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  rack: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'confirm'])

// Default to moving devices to unracked
const deleteOption = ref('move')

const confirmDelete = () => {
  const moveDevicesToUnracked = deleteOption.value === 'move'
  emit('confirm', moveDevicesToUnracked)
}
</script>
