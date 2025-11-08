<template>
  <div class="flex h-screen" style="background-color: var(--color-background);">
    <!-- Toast Notifications -->
    <Toast position="top-right" />

    <!-- Left Sidebar - Device Library -->
    <DeviceLibrary class="w-80 flex-shrink-0" />

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col overflow-hidden relative" :style="{ paddingRight: unrackedPanelWidth }">
      <!-- Top Menu Bar -->
      <header class="shadow-sm px-6 flex items-center justify-between transition-colors" style="background-color: var(--color-primary); min-height: 68px;">
        <h1 class="text-2xl font-bold leading-none" style="color: #0c0c0d;">RackSum</h1>
        <div class="flex gap-2 items-center">
          <!-- Dark Mode Toggle -->
          <button
            @click="toggleDarkMode"
            class="p-2 rounded transition-colors"
            style="color: #0c0c0d;"
            @mouseover="$event.target.style.backgroundColor = 'rgba(0, 0, 0, 0.1)'"
            @mouseout="$event.target.style.backgroundColor = 'transparent'"
            title="Toggle dark mode"
          >
            <svg v-if="!isDark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </button>

          <button
            @click="openSaveDialog"
            class="px-4 py-2 rounded transition-colors font-medium"
            style="background-color: rgba(0, 0, 0, 0.1); color: #0c0c0d;"
            @mouseover="$event.target.style.backgroundColor = 'rgba(0, 0, 0, 0.2)'"
            @mouseout="$event.target.style.backgroundColor = 'rgba(0, 0, 0, 0.1)'"
            title="Save to database"
          >
            Save
          </button>
          <button
            @click="openLoadDialog"
            class="px-4 py-2 rounded transition-colors font-medium"
            style="background-color: rgba(0, 0, 0, 0.1); color: #0c0c0d;"
            @mouseover="$event.target.style.backgroundColor = 'rgba(0, 0, 0, 0.2)'"
            @mouseout="$event.target.style.backgroundColor = 'rgba(0, 0, 0, 0.1)'"
            title="Load from database"
          >
            Load
          </button>
          <button
            @click="showConfig = true"
            class="px-4 py-2 rounded transition-colors font-medium"
            style="background-color: rgba(0, 0, 0, 0.1); color: #0c0c0d;"
            @mouseover="$event.target.style.backgroundColor = 'rgba(0, 0, 0, 0.2)'"
            @mouseout="$event.target.style.backgroundColor = 'rgba(0, 0, 0, 0.1)'"
          >
            Configure
          </button>
          <button
            @click="showImportExport = true"
            class="px-4 py-2 rounded transition-colors font-medium"
            style="background-color: rgba(0, 0, 0, 0.1); color: #0c0c0d;"
            @mouseover="$event.target.style.backgroundColor = 'rgba(0, 0, 0, 0.2)'"
            @mouseout="$event.target.style.backgroundColor = 'rgba(0, 0, 0, 0.1)'"
          >
            Import/Export
          </button>
        </div>
      </header>

      <!-- Rack Container -->
      <main class="flex-1 overflow-auto p-6">
        <RackContainer />
      </main>
    </div>

    <!-- Utilization Panel (fixed position, bottom-right) -->
    <UtilizationPanel />

    <!-- Right Sidebar - Unracked Devices (fixed position) -->
    <UnrackedDevices />

    <!-- Modals -->
    <ConfigMenu v-if="showConfig" @close="showConfig = false" />
    <ImportExport v-if="showImportExport" @close="showImportExport = false" />
    <SaveLoadDialog
      v-model="showSaveLoad"
      :mode="saveLoadMode"
      :current-config="currentConfig"
      @config-loaded="handleConfigLoaded"
    />
  </div>
</template>

<script setup>
import { ref, provide, computed } from 'vue'
import Toast from 'primevue/toast'
import DeviceLibrary from './components/DeviceLibrary.vue'
import RackContainer from './components/RackContainer.vue'
import UtilizationPanel from './components/UtilizationPanel.vue'
import UnrackedDevices from './components/UnrackedDevices.vue'
import ConfigMenu from './components/ConfigMenu.vue'
import ImportExport from './components/ImportExport.vue'
import SaveLoadDialog from './components/SaveLoadDialog.vue'
import { useDarkMode } from './composables/useDarkMode'
import { useRackConfig } from './composables/useRackConfig'
import { useDatabase } from './composables/useDatabase'

const showConfig = ref(false)
const showImportExport = ref(false)
const showSaveLoad = ref(false)
const saveLoadMode = ref('save')

// Dark mode
const { isDark, toggle: toggleDarkMode } = useDarkMode()

// Rack configuration
const { config, loadConfiguration } = useRackConfig()

// Database
const { loadCurrentSite } = useDatabase()

// Load current site on mount
loadCurrentSite()

// Track unracked panel state
const unrackedPanelExpanded = ref(true)
provide('unrackedPanelExpanded', unrackedPanelExpanded)

const unrackedPanelWidth = computed(() => {
  return unrackedPanelExpanded.value ? '320px' : '64px'
})

// Get current configuration for saving
const currentConfig = computed(() => config.value)

// Save/Load functions
function openSaveDialog() {
  saveLoadMode.value = 'save'
  showSaveLoad.value = true
}

function openLoadDialog() {
  saveLoadMode.value = 'load'
  showSaveLoad.value = true
}

function handleConfigLoaded(configData) {
  loadConfiguration(configData)
}
</script>