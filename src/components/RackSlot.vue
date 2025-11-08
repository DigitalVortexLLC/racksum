<template>
  <div
    @dragover.prevent="handleDragOver"
    @dragleave="handleDragLeave"
    @drop="handleDrop"
    :draggable="device && isFirstRU"
    @dragstart="handleDragStart"
    :class="slotClasses"
    class="relative flex items-center border transition-colors"
    :style="slotStyle"
  >
    <!-- Position number (only shown on first RU of device or empty slot) -->
    <div
      v-if="showPositionNumber"
      class="flex-shrink-0 w-8 text-xs text-gray-400 font-mono pl-1"
      :class="{ 'text-white': device }"
    >
      {{ position }}
    </div>

    <!-- Device content (only shown on first RU of device) -->
    <div
      v-if="device && isFirstRU"
      class="flex-1 pr-2 py-1 flex items-center justify-between min-w-0"
    >
      <span class="text-xs font-medium text-white truncate">
        {{ device.customName || device.name }}
      </span>
      <button
        @click="removeDevice"
        class="text-white hover:text-red-200 ml-2 flex-shrink-0"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useDragDrop } from '../composables/useDragDrop'
import { useRackConfig } from '../composables/useRackConfig'

const props = defineProps({
  rackId: {
    type: String,
    required: true
  },
  position: {
    type: Number,
    required: true
  },
  device: {
    type: Object,
    default: null
  }
})

const isDragOver = ref(false)
const { canDrop, handleDrop: drop, startDrag } = useDragDrop()
const { removeDeviceFromRack } = useRackConfig()

const isFirstRU = computed(() => {
  if (!props.device) return false
  return props.position === props.device.position
})

const showPositionNumber = computed(() => {
  return !props.device || isFirstRU.value
})

const slotClasses = computed(() => {
  const classes = []

  if (props.device) {
    // Device is present
    classes.push('h-6')
    if (!isFirstRU.value) {
      classes.push('border-t-0') // Connect multi-RU devices visually
    }
    if (isFirstRU.value) {
      classes.push('cursor-move') // Make it clear the device can be dragged
    }
  } else {
    // Empty slot
    classes.push('h-6 border-dashed')
    if (isDragOver.value) {
      classes.push('drag-over')
    }
  }

  return classes.join(' ')
})

const slotStyle = computed(() => {
  if (props.device) {
    return {
      backgroundColor: props.device.color,
      borderColor: props.device.color
    }
  }
  // Empty slot styling
  return {
    backgroundColor: 'var(--bg-secondary)',
    borderColor: 'var(--border-color)'
  }
})

const handleDragStart = (event) => {
  if (props.device && isFirstRU.value) {
    startDrag(event, props.device, {
      type: 'rack',
      rackId: props.rackId,
      position: props.position
    })
  }
}

const handleDragOver = (event) => {
  if (!props.device) {
    isDragOver.value = true
  }
}

const handleDragLeave = () => {
  isDragOver.value = false
}

const handleDrop = (event) => {
  isDragOver.value = false
  drop(event, props.rackId, props.position)
}

const removeDevice = () => {
  if (props.device) {
    removeDeviceFromRack(props.rackId, props.device.instanceId)
  }
}
</script>