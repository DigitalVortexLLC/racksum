<template>
  <div
    class="card bg-base-200 shadow-lg p-4 flex-shrink-0 w-[250px] cursor-move transition-all duration-200 hover:shadow-xl hover:scale-[1.02] border-2"
    :class="{
      'border-primary': isDragging || isDropTarget,
      'border-transparent': !isDragging && !isDropTarget,
      'opacity-50': isDragging
    }"
    draggable="true"
    @dragstart="handleDragStart"
    @dragend="handleDragEnd"
    @dragover.prevent="handleDragOver"
    @dragleave="handleDragLeave"
    @drop="handleDrop"
  >
    <!-- Rack Header -->
    <div class="mb-4 pb-2 flex items-center justify-between border-b border-base-300">
      <input
        v-model="rackName"
        class="input input-ghost text-lg font-semibold flex-1 px-2 py-1 h-auto min-h-0"
        @blur="updateRackName"
        @click.stop
        @mousedown.stop
      >
      <div class="flex gap-1">
        <button
          class="btn btn-ghost btn-sm btn-square text-primary"
          title="Configure rack"
          @click.stop="$emit('configure', rack)"
        >
          <svg
            class="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
            />
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
            />
          </svg>
        </button>
        <button
          class="btn btn-ghost btn-sm btn-square text-error"
          title="Delete rack"
          @click.stop="showDeleteModal = true"
        >
          <svg
            class="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
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
import { logError, logWarn, logInfo, logDebug } from '../utils/logger'

const props = defineProps({
  rack: {
    type: Object,
    required: true
  },
  index: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['reorder', 'configure'])

const { config, updateRack, deleteRack } = useRackConfig()
const { showSuccess } = useToast()

const showDeleteModal = ref(false)
const isDragging = ref(false)
const isDropTarget = ref(false)
const rackName = ref(props.rack.name)

const totalRU = computed(() => props.rack.ruSize || config.value.settings.ruPerRack || 42)

const getDeviceAtPosition = (position) => {
  return props.rack.devices.find(device => {
    const deviceEnd = device.position + device.ruSize - 1
    return position >= device.position && position <= deviceEnd
  })
}

const updateRackName = () => {
  updateRack(props.rack.id, { name: rackName.value })
}

const handleDragStart = (event) => {
  isDragging.value = true
  event.dataTransfer.effectAllowed = 'move'
  event.dataTransfer.setData('text/plain', JSON.stringify({
    type: 'rack',
    index: props.index,
    rackId: props.rack.id
  }))
}

const handleDragEnd = () => {
  isDragging.value = false
}

const handleDragOver = (event) => {
  const data = event.dataTransfer.types.includes('text/plain')
  if (data) {
    isDropTarget.value = true
  }
}

const handleDragLeave = () => {
  isDropTarget.value = false
}

const handleDrop = (event) => {
  event.preventDefault()
  isDropTarget.value = false
  
  try {
    const data = JSON.parse(event.dataTransfer.getData('text/plain'))
    if (data.type === 'rack' && data.index !== props.index) {
      emit('reorder', data.index, props.index)
    }
  } catch (e) {
    logError('Failed to parse drag data', e)
  }
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