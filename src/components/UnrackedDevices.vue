<template>
  <aside
    class="shadow-lg transition-all duration-300 flex flex-col bg-base-100 border-t border-base-300"
    :class="[isExpanded ? 'h-64' : 'h-16', { 'drop-zone-active': isDragOver }]"
    @dragover.prevent="handleDragOver"
    @dragleave="handleDragLeave"
    @drop="handleDrop"
  >
    <!-- Header with Toggle -->
    <div
      class="px-6 border-b border-base-300 transition-colors relative flex items-center bg-primary h-16"
      :class="{ 'cursor-pointer hover:opacity-90': isExpanded }"
      @click="isExpanded ? isExpanded = false : null"
    >
      <div
        v-if="isExpanded"
        class="flex items-center justify-between w-full"
      >
        <div class="flex items-center gap-4">
          <h2 class="text-xl font-bold text-primary-content">
            Unracked Devices
          </h2>
          <p class="text-sm text-primary-content/70">
            {{ unrackedDevices.length + unrackedProviders.length }} item{{ (unrackedDevices.length + unrackedProviders.length) !== 1 ? 's' : '' }}
          </p>
        </div>
        <button class="btn btn-ghost btn-sm btn-square text-primary-content/70 hover:text-primary-content">
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
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </button>
      </div>

      <!-- Collapsed View - Just Icon and Count -->
      <div
        v-else
        class="flex items-center justify-between w-full"
      >
        <div class="flex items-center gap-3">
          <svg
            class="w-6 h-6 text-primary-content"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"
            />
          </svg>
          <span class="text-primary-content font-semibold">Unracked Devices</span>
          <span
            v-if="unrackedDevices.length + unrackedProviders.length > 0"
            class="badge badge-error text-xs font-bold"
          >
            {{ unrackedDevices.length + unrackedProviders.length }}
          </span>
        </div>
        <button 
          class="btn btn-ghost btn-sm btn-square text-primary-content/70 hover:text-primary-content"
          @click.stop="isExpanded = true"
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
              d="M5 15l7-7 7 7"
            />
          </svg>
        </button>
      </div>
    </div>

    <div
      v-show="isExpanded"
      class="p-4 flex-1 overflow-y-auto overflow-x-auto"
    >
      <div
        v-if="unrackedDevices.length === 0 && unrackedProviders.length === 0"
        class="text-center py-8 text-base-content/60"
      >
        <svg
          class="w-12 h-12 mx-auto mb-2"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M5 13l4 4L19 7"
          />
        </svg>
        <p class="text-sm">
          All devices racked
        </p>
      </div>

      <div
        v-else
        class="flex gap-2 flex-wrap"
      >
        <!-- Devices -->
        <div
          v-for="device in unrackedDevices"
          :key="device.instanceId"
          :draggable="true"
          class="p-3 rounded cursor-move transition-colors border border-base-300 bg-primary/10 hover:bg-primary/20 flex items-center gap-3 min-w-[200px]"
          @dragstart="handleDragStart($event, device)"
        >
          <div class="flex items-center gap-3">
            <!-- Color indicator -->
            <div
              :style="{ backgroundColor: device.color }"
              class="w-4 h-4 rounded flex-shrink-0"
            />

            <!-- Device info -->
            <div class="flex-1 min-w-0">
              <div class="font-medium text-sm truncate">
                {{ device.customName || device.name }}
              </div>
              <div class="text-xs text-base-content/60">
                {{ device.ruSize }}U • {{ device.powerDraw }}W
              </div>
            </div>

            <!-- Remove button -->
            <button
              class="btn btn-ghost btn-xs btn-square text-error hover:text-error flex-shrink-0"
              title="Remove device"
              @click="removeDevice(device.instanceId)"
            >
              <svg
                class="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
            </button>
          </div>
        </div>

        <!-- Providers -->
        <div
          v-for="provider in unrackedProviders"
          :key="provider.id"
          class="p-3 rounded transition-colors border border-base-300 bg-success/10 hover:bg-success/20 flex items-center gap-3 min-w-[200px]"
        >
          <div class="flex items-center gap-3">
            <!-- Provider icon -->
            <svg
              v-if="provider.type === 'power'"
              class="w-5 h-5 text-success flex-shrink-0"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z"
                clip-rule="evenodd"
              />
            </svg>
            <svg
              v-else-if="provider.type === 'cooling'"
              class="w-5 h-5 text-success flex-shrink-0"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M10 2a1 1 0 011 1v1.323l3.954 1.582 1.599-.8a1 1 0 01.894 1.79l-1.233.616 1.738 5.42a1 1 0 01-.285 1.05A3.989 3.989 0 0115 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.715-5.349L11 6.477V9a1 1 0 11-2 0V6.477L6.237 7.582l1.715 5.349a1 1 0 01-.285 1.05A3.989 3.989 0 015 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.738-5.42-1.233-.617a1 1 0 01.894-1.788l1.599.799L9 4.323V3a1 1 0 011-1zm-5 8.274l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L5 10.274zm10 0l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L15 10.274z"
                clip-rule="evenodd"
              />
            </svg>
            <svg
              v-else-if="provider.type === 'network'"
              class="w-5 h-5 text-success flex-shrink-0"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
            </svg>

            <!-- Provider info -->
            <div class="flex-1 min-w-0">
              <div class="font-medium text-sm truncate">
                {{ provider.name }}
              </div>
              <div class="text-xs text-base-content/60">
                <span v-if="provider.powerCapacity > 0">{{ provider.powerCapacity.toLocaleString() }}W</span>
                <span v-if="provider.coolingCapacity > 0">{{ (provider.coolingCapacity / 12000).toFixed(1) }} Tons</span>
                <span v-if="provider.networkCapacity > 0">{{ provider.networkCapacity }} Gbps</span>
              </div>
            </div>

            <!-- Remove button -->
            <button
              class="btn btn-ghost btn-xs btn-square text-error hover:text-error flex-shrink-0"
              title="Remove provider"
              @click="removeProvider(provider.id)"
            >
              <svg
                class="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Helper text -->
      <div
        v-if="unrackedDevices.length > 0"
        class="alert alert-info mt-4"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          class="stroke-current shrink-0 w-5 h-5"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <span class="text-xs">Drag devices from here into racks to assign them positions.</span>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed, inject, watch } from 'vue'
import { useRackConfig } from '../composables/useRackConfig'
import { useResourceProviders } from '../composables/useResourceProviders'
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
const { getUnrackedProviders, deleteProvider } = useResourceProviders()
const { startDrag, handleDropToUnracked, dragSource } = useDragDrop()
const { showSuccess, showInfo } = useToast()

const unrackedProviders = getUnrackedProviders

const handleDragStart = (event, device) => {
  startDrag(event, device, { type: 'unracked' })
}

const handleDragOver = (event) => {
  // Show drop zone if dragging from a rack or from provider library
  if (dragSource.value?.type === 'rack' || dragSource.value?.type === 'provider-library') {
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

const removeProvider = (providerId) => {
  const provider = unrackedProviders.value.find(p => p.id === providerId)
  if (confirm('Remove this provider permanently?')) {
    deleteProvider(providerId)
    showSuccess('Provider removed', `${provider?.name || 'Provider'} has been removed`)
  }
}
</script>

<style scoped>
.drop-zone-active {
  box-shadow: inset 0 0 0 3px oklch(var(--p));
  transition: box-shadow 0.2s ease;
}
</style>