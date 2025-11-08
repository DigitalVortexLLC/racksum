<template>
  <div
    :draggable="true"
    @dragstart="handleDragStart"
    class="p-3 cursor-move transition-colors last:border-b-0"
    style="border-bottom: 1px solid var(--border-color);"
    @mouseover="$event.target.style.backgroundColor = 'var(--bg-secondary)'"
    @mouseout="$event.target.style.backgroundColor = 'transparent'"
  >
    <div class="flex items-center gap-3">
      <!-- Color indicator -->
      <div
        :style="{ backgroundColor: device.color }"
        class="w-4 h-4 rounded flex-shrink-0"
      ></div>

      <!-- Device info -->
      <div class="flex-1 min-w-0">
        <div class="font-medium text-sm truncate" style="color: var(--text-primary);">
          {{ device.name }}
        </div>
        <div class="text-xs" style="color: var(--text-secondary);">
          {{ device.ruSize }}U • {{ device.powerDraw }}W
        </div>
      </div>
    </div>

    <!-- Tooltip on hover -->
    <div v-if="showTooltip" class="text-xs mt-2" style="color: var(--text-secondary);">
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