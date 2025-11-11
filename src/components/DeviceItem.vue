<template>
  <div
    :draggable="true"
    class="p-3 cursor-move transition-colors border-b border-base-300 last:border-b-0 hover:bg-base-200"
    @dragstart="handleDragStart"
  >
    <div class="flex items-center gap-3">
      <!-- Color indicator -->
      <div
        :style="{ backgroundColor: device.color }"
        class="size-4 rounded flex-shrink-0"
      />

      <!-- Device info -->
      <div class="flex-1 min-w-0">
        <div class="font-medium text-sm truncate">
          {{ device.name }}
        </div>
        <div class="text-xs opacity-70">
          {{ device.ruSize }}U • {{ device.powerDraw }}W
        </div>
      </div>
    </div>

    <!-- Tooltip on hover -->
    <div
      v-if="showTooltip"
      class="text-xs mt-2 opacity-70"
    >
      {{ device.description }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useDragDrop } from '../composables/useDragDrop'

const props = defineProps({
  device: {
    type: Object,
    required: true
  }
})

const showTooltip = ref(false)
const { startDrag } = useDragDrop()

const handleDragStart = (event) => {
  startDrag(event, props.device)
}
</script>