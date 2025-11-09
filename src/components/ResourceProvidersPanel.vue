<template>
  <div
    class="fixed top-4 left-4 z-10 rounded-lg shadow-lg transition-all duration-300"
    :class="isExpanded ? 'w-80' : 'w-16'"
    style="background-color: var(--bg-primary);"
  >
    <!-- Header with Toggle -->
    <div
      class="flex items-center justify-between p-4 cursor-pointer transition-colors rounded-t-lg"
      style="color: var(--text-primary);"
      @click="isExpanded = !isExpanded"
      @mouseover="$event.target.style.backgroundColor = 'var(--bg-secondary)'"
      @mouseout="$event.target.style.backgroundColor = 'transparent'"
    >
      <div class="flex items-center gap-2">
        <svg class="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd" />
        </svg>
        <h3 v-if="isExpanded" class="text-lg font-semibold">Resource Providers</h3>
      </div>
      <button v-if="isExpanded" style="color: var(--text-secondary);">
        <svg
          class="w-5 h-5 transition-transform duration-300"
          :class="{ 'rotate-180': isExpanded }"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
    </div>

    <!-- Expanded Content -->
    <div v-if="isExpanded" class="px-4 pb-4 space-y-2">
      <!-- No providers message -->
      <div v-if="resourceProviders.length === 0" class="text-center py-6">
        <p class="text-sm mb-2" style="color: var(--text-secondary);">
          No resource providers configured
        </p>
        <p class="text-xs" style="color: var(--text-secondary);">
          Add providers in Device Manager
        </p>
      </div>

      <!-- Provider list -->
      <div
        v-for="provider in resourceProviders"
        :key="provider.id"
        class="p-3 rounded border transition-colors"
        style="background-color: var(--bg-secondary); border-color: var(--border-color);"
        @mouseover="$event.target.style.borderColor = 'var(--color-primary)'"
        @mouseout="$event.target.style.borderColor = 'var(--border-color)'"
      >
        <div class="flex items-start gap-3">
          <!-- Icon -->
          <div class="flex-shrink-0 mt-0.5">
            <svg v-if="provider.type === 'power'" class="w-5 h-5" style="color: var(--color-primary);" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd" />
            </svg>
            <svg v-else-if="provider.type === 'cooling'" class="w-5 h-5" style="color: var(--color-primary);" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1.323l3.954 1.582 1.599-.8a1 1 0 01.894 1.79l-1.233.616 1.738 5.42a1 1 0 01-.285 1.05A3.989 3.989 0 0115 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.715-5.349L11 6.477V9a1 1 0 11-2 0V6.477L6.237 7.582l1.715 5.349a1 1 0 01-.285 1.05A3.989 3.989 0 015 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.738-5.42-1.233-.617a1 1 0 01.894-1.788l1.599.799L9 4.323V3a1 1 0 011-1zm-5 8.274l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L5 10.274zm10 0l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L15 10.274z" clip-rule="evenodd" />
            </svg>
            <svg v-else-if="provider.type === 'network'" class="w-5 h-5" style="color: var(--color-primary);" fill="currentColor" viewBox="0 0 20 20">
              <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
            </svg>
          </div>

          <!-- Info -->
          <div class="flex-1 min-w-0">
            <div class="font-medium text-sm truncate" style="color: var(--text-primary);">
              {{ provider.name }}
            </div>
            <div class="text-xs" style="color: var(--text-secondary);">
              <span v-if="provider.powerCapacity > 0">{{ provider.powerCapacity.toLocaleString() }}W</span>
              <span v-if="provider.powerPortsCapacity > 0" class="ml-2">{{ provider.powerPortsCapacity }} ports</span>
              <span v-if="provider.coolingCapacity > 0">{{ (provider.coolingCapacity / 12000).toFixed(1) }} Tons</span>
              <span v-if="provider.networkCapacity > 0">{{ provider.networkCapacity }} Gbps</span>
            </div>
            <div v-if="provider.location" class="text-xs mt-1 truncate" style="color: var(--text-secondary);">
              📍 {{ provider.location }}
            </div>
          </div>
        </div>
      </div>

      <!-- Summary -->
      <div
        v-if="resourceProviders.length > 0"
        class="mt-4 pt-4 border-t"
        style="border-color: var(--border-color);"
      >
        <div class="text-sm font-medium mb-2" style="color: var(--text-primary);">
          Total Capacity
        </div>
        <div class="space-y-1 text-xs" style="color: var(--text-secondary);">
          <div v-if="totalPowerCapacity > 0" class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd" />
            </svg>
            <span>{{ totalPowerCapacity.toLocaleString() }}W</span>
          </div>
          <div v-if="totalPowerPortsCapacity > 0" class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd" />
            </svg>
            <span>{{ totalPowerPortsCapacity }} power ports</span>
          </div>
          <div v-if="totalCoolingCapacity > 0" class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1.323l3.954 1.582 1.599-.8a1 1 0 01.894 1.79l-1.233.616 1.738 5.42a1 1 0 01-.285 1.05A3.989 3.989 0 0115 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.715-5.349L11 6.477V9a1 1 0 11-2 0V6.477L6.237 7.582l1.715 5.349a1 1 0 01-.285 1.05A3.989 3.989 0 015 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.738-5.42-1.233-.617a1 1 0 01.894-1.788l1.599.799L9 4.323V3a1 1 0 011-1zm-5 8.274l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L5 10.274zm10 0l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L15 10.274z" clip-rule="evenodd" />
            </svg>
            <span>{{ (totalCoolingCapacity / 12000).toFixed(1) }} Tons</span>
          </div>
          <div v-if="totalNetworkCapacity > 0" class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
            </svg>
            <span>{{ totalNetworkCapacity }} Gbps</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Collapsed indicator -->
    <div v-if="!isExpanded && resourceProviders.length > 0" class="px-4 pb-4">
      <div class="flex flex-col items-center gap-2">
        <div class="w-2 h-2 rounded-full bg-green-500"></div>
        <span class="text-xs font-medium" style="color: var(--text-primary);">
          {{ resourceProviders.length }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, provide } from 'vue'
import { useResourceProviders } from '../composables/useResourceProviders'

const {
  resourceProviders,
  totalPowerCapacity,
  totalPowerPortsCapacity,
  totalCoolingCapacity,
  totalNetworkCapacity
} = useResourceProviders()

const isExpanded = ref(true)

// Provide the expanded state for other components to adjust their positioning
provide('resourceProvidersExpanded', isExpanded)
</script>
