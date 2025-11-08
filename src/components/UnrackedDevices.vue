<template>
  <aside
    class="shadow-lg transition-all duration-300 flex flex-col fixed right-0 top-0 h-screen z-10"
    :class="[isExpanded ? 'w-80' : 'w-16', { 'drop-zone-active': isDragOver }]"
    :style="{ backgroundColor: 'var(--bg-primary)', borderLeft: '1px solid var(--border-color)' }"
    @dragover.prevent="handleDragOver"
    @dragleave="handleDragLeave"
    @drop="handleDrop"
  >
    <!-- Header with Toggle -->
    <div
      class="px-6 border-b transition-colors relative flex items-center"
      :class="{ 'cursor-pointer': isExpanded }"
      style="background-color: var(--color-primary); min-height: 68px;"
      @click="isExpanded ? isExpanded = false : null"
      @mouseover="isExpanded ? $event.target.style.opacity = '0.9' : null"
      @mouseout="isExpanded ? $event.target.style.opacity = '1' : null"
    >
      <div v-if="isExpanded" class="flex items-center justify-between w-full py-4">
        <div>
          <h2 class="text-2xl font-bold leading-none" style="color: #0c0c0d;">Unracked Devices</h2>
          <p class="text-xs mt-1" style="color: rgba(12, 12, 13, 0.7);">
            {{ unrackedDevices.length }} device{{ unrackedDevices.length !== 1 ? 's' : '' }}
          </p>
        </div>
        <button style="color: rgba(12, 12, 13, 0.7);" @mouseover="$event.target.style.color = '#0c0c0d'" @mouseout="$event.target.style.color = 'rgba(12, 12, 13, 0.7)'">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
      </div>

      <!-- Collapsed View - Just Icon -->
      <div v-else class="flex items-center justify-center w-full">
        <!-- Icon with Badge -->
        <div class="relative">
          <svg class="w-6 h-6" style="color: #0c0c0d;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
          </svg>
          <!-- Notification Badge -->
          <span
            v-if="unrackedDevices.length > 0"
            class="absolute -top-2 -right-2 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center"
            style="background-color: #ef4444;"
          >
            {{ unrackedDevices.length > 9 ? '9+' : unrackedDevices.length }}
          </span>
        </div>
      </div>
    </div>

    <div v-show="isExpanded" class="p-4 flex-1 overflow-y-auto">
      <div v-if="unrackedDevices.length === 0" class="text-center py-8" style="color: var(--text-secondary);">
        <svg class="w-12 h-12 mx-auto mb-2" style="color: var(--text-secondary);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        <p class="text-sm">All devices racked</p>
      </div>

      <div v-else class="space-y-2">
        <div
          v-for="device in unrackedDevices"
          :key="device.instanceId"
          :draggable="true"
          @dragstart="handleDragStart($event, device)"
          class="p-3 rounded cursor-move transition-colors border"
          style="background-color: rgba(132, 204, 22, 0.08); border-color: var(--border-color);"
          @mouseover="$event.target.style.backgroundColor = 'rgba(132, 204, 22, 0.12)'"
          @mouseout="$event.target.style.backgroundColor = 'rgba(132, 204, 22, 0.08)'"
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
                {{ device.customName || device.name }}
              </div>
              <div class="text-xs" style="color: var(--text-secondary);">
                {{ device.ruSize }}U • {{ device.powerDraw }}W
              </div>
            </div>

            <!-- Remove button -->
            <button
              @click="removeDevice(device.instanceId)"
              class="flex-shrink-0 transition-colors"
              style="color: #ef4444;"
              @mouseover="$event.target.style.color = '#dc2626'"
              @mouseout="$event.target.style.color = '#ef4444'"
              title="Remove device"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>

          <div v-if="device.description" class="text-xs mt-2" style="color: var(--text-secondary);">
            {{ device.description }}
          </div>
        </div>
      </div>

      <!-- Helper text -->
      <div
        v-if="unrackedDevices.length > 0"
        class="mt-4 p-3 rounded border"
        style="background-color: rgba(132, 204, 22, 0.1); border-color: var(--border-color);"
      >
        <p class="text-xs" style="color: var(--color-primary-dark);">
          💡 Drag devices from here into racks to assign them positions.
        </p>
      </div>
    </div>

    <!-- Expand Arrow Button (bottom of panel when collapsed) -->
    <div
      v-if="!isExpanded"
      class="mt-auto p-4 cursor-pointer transition-colors flex items-center justify-center"
      style="background-color: var(--color-primary);"
      @click="isExpanded = true"
      @mouseover="$event.target.style.opacity = '0.9'"
      @mouseout="$event.target.style.opacity = '1'"
    >
      <svg class="w-5 h-5" style="color: #0c0c0d;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed, inject, watch } from 'vue'
import { useRackConfig } from '../composables/useRackConfig'
import { useDragDrop } from '../composables/useDragDrop'
import { useToast } from '../composables/useToast'

const isExpanded = ref(false)
const isDragOver = ref(false)
const unrackedPanelExpanded = inject('unrackedPanelExpanded', ref(true))

// Sync with parent
watch(isExpanded, (newValue) => {
  unrackedPanelExpanded.value = newValue
})

const { unrackedDevices, removeUnrackedDevice } = useRackConfig()
const { startDrag, handleDropToUnracked, dragSource } = useDragDrop()
const { showSuccess, showInfo } = useToast()

const handleDragStart = (event, device) => {
  startDrag(event, device, { type: 'unracked' })
}

const handleDragOver = (event) => {
  // Only show drop zone if dragging from a rack
  if (dragSource.value?.type === 'rack') {
    isDragOver.value = true
  }
}

const handleDragLeave = (event) => {
  isDragOver.value = false
}

const handleDrop = (event) => {
  isDragOver.value = false
  handleDropToUnracked(event)
}

const removeDevice = (instanceId) => {
  const device = unrackedDevices.value.find(d => d.instanceId === instanceId)
  if (confirm('Remove this device permanently?')) {
    removeUnrackedDevice(instanceId)
    showSuccess('Device removed', `${device?.customName || device?.name || 'Device'} has been removed`)
  }
}
</script>

<style scoped>
.drop-zone-active {
  box-shadow: inset 0 0 0 3px var(--color-primary);
  transition: box-shadow 0.2s ease;
}
</style>