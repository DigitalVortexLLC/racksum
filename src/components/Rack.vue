<template>
  <div class="rounded-lg shadow-lg p-4 flex-shrink-0 transition-colors" style="width: 250px; background-color: var(--bg-primary);">
    <!-- Rack Header -->
    <div class="mb-4 pb-2 flex items-center justify-between" style="border-bottom: 1px solid var(--border-color);">
      <input
        v-model="rack.name"
        class="text-lg font-semibold flex-1 focus:outline-none px-2 py-1 rounded transition-colors"
        style="background-color: transparent; color: var(--text-primary);"
        @blur="updateRackName"
        @focus="$event.target.style.backgroundColor = 'var(--bg-secondary)'"
      />
      <button
        @click="showDeleteModal = true"
        class="ml-2 p-1 rounded transition-colors hover:bg-red-100"
        style="color: #ef4444;"
        title="Delete rack"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- Rack Slots (numbered from top to bottom) -->
    <div class="space-y-0.5">
      <RackSlot
        v-for="position in totalRU"
        :key="position"
        :rack-id="rack.id"
        :position="position"
        :device="getDeviceAtPosition(position)"
      />
    </div>

    <!-- Delete Rack Modal -->
    <DeleteRackModal
      v-if="showDeleteModal"
      :rack="rack"
      @close="showDeleteModal = false"
      @confirm="handleDeleteConfirm"
    />
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRackConfig } from '../composables/useRackConfig'
import { useToast } from '../composables/useToast'
import RackSlot from './RackSlot.vue'
import DeleteRackModal from './DeleteRackModal.vue'

const props = defineProps({
  rack: {
    type: Object,
    required: true
  }
})

const { config, updateRack, deleteRack } = useRackConfig()
const { showSuccess } = useToast()

const showDeleteModal = ref(false)

const totalRU = computed(() => config.value.settings.ruPerRack || 42)

const getDeviceAtPosition = (position) => {
  return props.rack.devices.find(device => {
    const deviceEnd = device.position + device.ruSize - 1
    return position >= device.position && position <= deviceEnd
  })
}

const updateRackName = () => {
  updateRack(props.rack.id, { name: props.rack.name })
}

const handleDeleteConfirm = (moveDevicesToUnracked) => {
  const rackName = props.rack.name
  const deviceCount = props.rack.devices.length

  deleteRack(props.rack.id, moveDevicesToUnracked)
  showDeleteModal.value = false

  if (deviceCount > 0) {
    if (moveDevicesToUnracked) {
      showSuccess('Rack Deleted', `${rackName} deleted and ${deviceCount} device${deviceCount > 1 ? 's' : ''} moved to unracked`)
    } else {
      showSuccess('Rack Deleted', `${rackName} and ${deviceCount} device${deviceCount > 1 ? 's' : ''} deleted`)
    }
  } else {
    showSuccess('Rack Deleted', `${rackName} deleted`)
  }
}
</script>