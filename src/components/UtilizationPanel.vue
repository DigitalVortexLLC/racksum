<template>
  <div
    class="rounded-lg shadow-lg transition-all duration-300 fixed bottom-4 z-10"
    :class="isExpanded ? 'w-80' : 'w-auto'"
    :style="{ right: unrackedPanelOffset, backgroundColor: 'var(--bg-primary)' }"
  >
    <!-- Header with Toggle -->
    <div
      class="flex items-center justify-between p-4 cursor-pointer transition-colors rounded-t-lg"
      style="color: var(--text-primary);"
      @click="isExpanded = !isExpanded"
      @mouseover="$event.target.style.backgroundColor = 'var(--bg-secondary)'"
      @mouseout="$event.target.style.backgroundColor = 'transparent'"
    >
      <h3 class="text-lg font-semibold">
        {{ isExpanded ? 'Resource Utilization' : 'Resources' }}
      </h3>
      <button style="color: var(--text-secondary);">
        <svg
          class="w-5 h-5 transition-transform duration-300"
          :class="{ 'rotate-180': isExpanded }"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </button>
    </div>

    <!-- Expandable Content -->
    <div
      v-show="isExpanded"
      class="px-4 pb-4"
    >
      <!-- Power Utilization -->
      <div class="mb-4">
        <div class="flex justify-between items-center mb-1">
          <span class="text-sm font-medium" style="color: var(--text-primary);">Power</span>
          <span class="text-sm" style="color: var(--text-secondary);">
            {{ powerUsed }}W / {{ powerCapacity }}W
          </span>
        </div>
        <div class="w-full rounded-full h-4 overflow-hidden" style="background-color: var(--border-color);">
          <div
            :class="powerBarColor"
            :style="{ width: powerPercentage + '%' }"
            class="h-full transition-all duration-300"
          ></div>
        </div>
        <div class="text-xs mt-1" style="color: var(--text-secondary);">{{ powerPercentage }}%</div>
      </div>

      <!-- HVAC Utilization -->
      <div class="mb-4">
        <div class="flex justify-between items-center mb-1">
          <span class="text-sm font-medium" style="color: var(--text-primary);">HVAC</span>
          <span class="text-sm" style="color: var(--text-secondary);">
            {{ hvacLoadTons }} / {{ hvacCapacityTons }} Tons
          </span>
        </div>
        <div class="w-full rounded-full h-4 overflow-hidden" style="background-color: var(--border-color);">
          <div
            :class="hvacBarColor"
            :style="{ width: hvacPercentage + '%' }"
            class="h-full transition-all duration-300"
          ></div>
        </div>
        <div class="text-xs mt-1" style="color: var(--text-secondary);">{{ hvacPercentage }}%</div>
      </div>

      <!-- RU Utilization -->
      <div>
        <div class="flex justify-between items-center mb-1">
          <span class="text-sm font-medium" style="color: var(--text-primary);">Rack Units</span>
          <span class="text-sm" style="color: var(--text-secondary);">
            {{ ruUsed }}U / {{ ruCapacity }}U
          </span>
        </div>
        <div class="w-full rounded-full h-4 overflow-hidden" style="background-color: var(--border-color);">
          <div
            :class="ruBarColor"
            :style="{ width: ruPercentage + '%' }"
            class="h-full transition-all duration-300"
          ></div>
        </div>
        <div class="text-xs mt-1" style="color: var(--text-secondary);">{{ ruPercentage }}%</div>
      </div>

      <!-- Details Button -->
      <div class="mt-4">
        <button
          @click.stop="showDetailModal = true"
          class="w-full py-2 px-4 rounded-lg text-sm font-medium transition-colors"
          style="background-color: var(--bg-secondary); color: var(--text-primary);"
          @mouseover="$event.target.style.backgroundColor = 'var(--border-color)'"
          @mouseout="$event.target.style.backgroundColor = 'var(--bg-secondary)'"
        >
          View Details
        </button>
      </div>
    </div>

    <!-- Compact View (when collapsed) -->
    <div
      v-show="!isExpanded"
      class="px-4 pb-4 flex flex-col gap-3"
    >
      <!-- Power Compact -->
      <div class="flex items-center gap-2 group relative">
        <div class="flex items-center gap-1.5">
          <!-- Lightning bolt icon for power -->
          <svg class="w-5 h-5" style="color: var(--text-primary);" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd" />
          </svg>
          <!-- Status LED -->
          <div class="w-2 h-2 rounded-full" :class="powerBarColor"></div>
        </div>
        <span class="text-sm font-medium" style="color: var(--text-primary);">{{ powerPercentage }}%</span>
        <!-- Tooltip -->
        <div class="absolute left-full ml-2 px-2 py-1 bg-gray-800 text-white text-xs rounded whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
          Power
        </div>
      </div>

      <!-- HVAC Compact -->
      <div class="flex items-center gap-2 group relative">
        <div class="flex items-center gap-1.5">
          <!-- Snowflake icon for HVAC/cooling -->
          <svg class="w-5 h-5" style="color: var(--text-primary);" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1.323l3.954 1.582 1.599-.8a1 1 0 01.894 1.79l-1.233.616 1.738 5.42a1 1 0 01-.285 1.05A3.989 3.989 0 0115 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.715-5.349L11 6.477V9a1 1 0 11-2 0V6.477L6.237 7.582l1.715 5.349a1 1 0 01-.285 1.05A3.989 3.989 0 015 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.738-5.42-1.233-.617a1 1 0 01.894-1.788l1.599.799L9 4.323V3a1 1 0 011-1zm-5 8.274l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L5 10.274zm10 0l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L15 10.274z" clip-rule="evenodd" />
          </svg>
          <!-- Status LED -->
          <div class="w-2 h-2 rounded-full" :class="hvacBarColor"></div>
        </div>
        <span class="text-sm font-medium" style="color: var(--text-primary);">{{ hvacPercentage }}%</span>
        <!-- Tooltip -->
        <div class="absolute left-full ml-2 px-2 py-1 bg-gray-800 text-white text-xs rounded whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
          HVAC
        </div>
      </div>

      <!-- RU Compact -->
      <div class="flex items-center gap-2 group relative">
        <div class="flex items-center gap-1.5">
          <!-- Server/rack icon for RU -->
          <svg class="w-5 h-5" style="color: var(--text-primary);" fill="currentColor" viewBox="0 0 20 20">
            <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1v-2zM3 16a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1v-2z" />
          </svg>
          <!-- Status LED -->
          <div class="w-2 h-2 rounded-full" :class="ruBarColor"></div>
        </div>
        <span class="text-sm font-medium" style="color: var(--text-primary);">{{ ruPercentage }}%</span>
        <!-- Tooltip -->
        <div class="absolute left-full ml-2 px-2 py-1 bg-gray-800 text-white text-xs rounded whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
          Rack Units
        </div>
      </div>
    </div>

    <!-- Resource Detail Modal -->
    <ResourceDetailModal v-model="showDetailModal" />
  </div>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import { useUtilization } from '../composables/useUtilization'
import { btuToTons } from '../utils/calculations'
import ResourceDetailModal from './ResourceDetailModal.vue'

const isExpanded = ref(false)
const showDetailModal = ref(false)
const unrackedPanelExpanded = inject('unrackedPanelExpanded', ref(true))

const unrackedPanelOffset = computed(() => {
  const baseOffset = 16 // 1rem in pixels (right-4)
  const panelWidth = unrackedPanelExpanded.value ? 320 : 64
  return `${baseOffset + panelWidth}px`
})

const {
  powerUsed,
  powerCapacity,
  powerPercentage,
  hvacLoad,
  hvacCapacity,
  hvacPercentage,
  ruUsed,
  ruCapacity,
  ruPercentage
} = useUtilization()

// Convert BTU/hr to Refrigeration Tons for display
const hvacLoadTons = computed(() => btuToTons(hvacLoad.value).toFixed(1))
const hvacCapacityTons = computed(() => btuToTons(hvacCapacity.value).toFixed(1))

const getBarColor = (percentage) => {
  if (percentage < 70) return 'bg-green-500'
  if (percentage < 90) return 'bg-yellow-500'
  return 'bg-red-500'
}

const powerBarColor = computed(() => getBarColor(powerPercentage.value))
const hvacBarColor = computed(() => getBarColor(hvacPercentage.value))
const ruBarColor = computed(() => getBarColor(ruPercentage.value))

// Text color versions for icons
const powerIconColor = computed(() => powerBarColor.value.replace('bg-', 'text-'))
const hvacIconColor = computed(() => hvacBarColor.value.replace('bg-', 'text-'))
const ruIconColor = computed(() => ruBarColor.value.replace('bg-', 'text-'))
</script>