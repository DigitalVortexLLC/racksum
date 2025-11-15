<template>
  <div class="flex h-screen bg-base-100">
    <!-- Toast Notifications -->
    <ToastContainer />

    <!-- Left Sidebar - Device Library -->
    <DeviceLibrary 
      class="w-80 flex-shrink-0"
      @open-device-manager="openDeviceManager"
    />

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Top Menu Bar -->
      <header
        class="navbar bg-primary shadow-sm px-6"
        style="min-height: 68px;"
      >
        <div class="navbar-start gap-4">
          <h1 class="text-2xl font-bold text-primary-content">
            Racker
          </h1>
          <div class="flex items-center gap-2">
            <span class="text-primary-content opacity-50">|</span>
            <div
              v-if="!isEditingSiteName"
              class="text-lg font-semibold cursor-pointer hover:opacity-80 transition-opacity px-2 py-1 rounded text-primary-content"
              :class="{ 'opacity-50 italic': !currentSite }"
              :title="currentSite ? 'Click to edit site name' : 'Click to add site name'"
              @click="startEditingSiteName"
            >
              {{ currentSite ? currentSite.name : 'Add site name...' }}
            </div>
            <input
              v-else
              ref="siteNameInput"
              v-model="editedSiteName"
              class="input input-sm input-bordered text-lg font-semibold bg-base-100 text-base-content"
              style="max-width: 300px;"
              placeholder="Enter site name..."
              @blur="finishEditingSiteName"
              @keyup.enter="finishEditingSiteName"
              @keyup.escape="cancelEditingSiteName"
            >
          </div>
        </div>
        <div class="navbar-end gap-2">
          <!-- Dark Mode Toggle -->
          <button
            class="btn btn-ghost btn-circle text-primary-content"
            title="Toggle dark mode"
            @click="toggleDarkMode"
          >
            <svg
              v-if="!isDark"
              class="size-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
              />
            </svg>
            <svg
              v-else
              class="size-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
              />
            </svg>
          </button>

          <!-- Save/Load buttons only show when auth is enabled -->
          <button
            v-if="authConfig.require_auth"
            class="btn btn-ghost text-primary-content"
            title="Save to database"
            @click="openSaveDialog"
          >
            Save
          </button>
          <button
            v-if="authConfig.require_auth"
            class="btn btn-ghost text-primary-content"
            title="Load from database"
            @click="openLoadDialog"
          >
            Load
          </button>
          <!-- Share button: shows when site exists (auth enabled) or when site name is set (auth disabled) -->
          <button
            v-if="currentSite && (authConfig.require_auth || currentSite.name)"
            class="btn btn-ghost text-primary-content"
            title="Share this site with a link"
            @click="shareCurrentSite"
          >
            <svg
              class="size-5 mr-1"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"
              />
            </svg>
            Share
          </button>
          <button
            class="btn btn-ghost text-primary-content"
            @click="showConfig = true"
          >
            Configure
          </button>
          <button
            class="btn btn-ghost text-primary-content"
            @click="showImportExport = true"
          >
            Import/Export
          </button>
          <!-- Documentation Links -->
          <button
            class="btn btn-ghost text-primary-content"
            title="View documentation"
            @click="navigateToDocs"
          >
            <svg
              class="size-5 mr-1"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
              />
            </svg>
            Docs
          </button>
          <button
            class="btn btn-ghost text-primary-content"
            title="View API documentation"
            @click="navigateToApiDocs"
          >
            <svg
              class="size-5 mr-1"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"
              />
            </svg>
            API
          </button>
          <button
            v-if="authConfig.require_auth && authConfig.passkey_supported"
            class="btn btn-square btn-ghost text-primary-content"
            title="Passkey Authentication"
            @click="showPasskeyAuth = true"
          >
            <svg
              class="size-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"
              />
            </svg>
          </button>
        </div>
      </header>

      <!-- Main content with rack container and unracked devices -->
      <div class="flex-1 flex flex-col overflow-hidden relative">
        <!-- Rack Container -->
        <main class="flex-1 overflow-auto p-6">
          <RackContainer />
        </main>

        <!-- Bottom Panel - Unracked Devices -->
        <UnrackedDevices />

        <!-- Utilization Panel (positioned in content area, top-right) -->
        <UtilizationPanel />
      </div>
    </div>

    <!-- Modals -->
    <ConfigMenu
      v-if="showConfig"
      @close="showConfig = false"
    />
    <ImportExport
      v-if="showImportExport"
      @close="showImportExport = false"
    />
    <DeviceManager 
      v-if="showDeviceManager" 
      :initial-tab="deviceManagerTab"
      @close="showDeviceManager = false" 
    />
    <SaveLoadDialog
      v-model="showSaveLoad"
      :mode="saveLoadMode"
      :current-config="currentConfig"
      @config-loaded="handleConfigLoaded"
    />
    <PasskeyAuth
      v-if="authConfig.require_auth && authConfig.passkey_supported"
      v-model="showPasskeyAuth"
      @authenticated="handleAuthenticated"
    />
  </div>
</template>

<script setup>
import { ref, provide, computed, onMounted } from 'vue'
import ToastContainer from './components/ToastContainer.vue'
import DeviceLibrary from './components/DeviceLibrary.vue'
import RackContainer from './components/RackContainer.vue'
import UtilizationPanel from './components/UtilizationPanel.vue'
import UnrackedDevices from './components/UnrackedDevices.vue'
import ConfigMenu from './components/ConfigMenu.vue'
import ImportExport from './components/ImportExport.vue'
import DeviceManager from './components/DeviceManager.vue'
import SaveLoadDialog from './components/SaveLoadDialog.vue'
import PasskeyAuth from './components/PasskeyAuth.vue'
import { useDarkMode } from './composables/useDarkMode'
import { useRackConfig } from './composables/useRackConfig'
import { useDatabase } from './composables/useDatabase'
import { usePasskey } from './composables/usePasskey'
import { useToast } from './composables/useToast'
import { logError, logWarn, logInfo, logDebug } from '@/utils/logger'

const showConfig = ref(false)
const showImportExport = ref(false)
const showDeviceManager = ref(false)
const deviceManagerTab = ref('groups')
const showSaveLoad = ref(false)
const showPasskeyAuth = ref(false)
const saveLoadMode = ref('save')

// Dark mode
const { isDark, toggle: toggleDarkMode } = useDarkMode()

// Rack configuration
const { config, loadConfiguration } = useRackConfig()

// Database
const { currentSite, loadCurrentSite, updateSite, createSite, setCurrentSite, fetchSiteByUuid } = useDatabase()

// Toast notifications
const { showToast } = useToast()

// Site name editing
const isEditingSiteName = ref(false)
const editedSiteName = ref('')
const siteNameInput = ref(null)

function startEditingSiteName() {
  editedSiteName.value = currentSite.value ? currentSite.value.name : ''
  isEditingSiteName.value = true
  setTimeout(() => {
    siteNameInput.value?.focus()
    siteNameInput.value?.select()
  }, 50)
}

async function finishEditingSiteName() {
  const newName = editedSiteName.value.trim()

  if (!newName) {
    cancelEditingSiteName()
    return
  }

  try {
    if (!currentSite.value) {
      // Create new site if none exists
      const newSite = await createSite(newName)
      setCurrentSite(newSite)
      if (!authConfig.value.require_auth) {
        showToast('success', `Site "${newName}" created - you can now share it!`)
      }
    } else if (newName !== currentSite.value.name) {
      // Update existing site
      await updateSite(currentSite.value.id, newName, currentSite.value.description)
      currentSite.value.name = newName
    }
  } catch (err) {
    logError('Failed to save site name', err)
    showToast('error', 'Failed to save site name')
  }

  isEditingSiteName.value = false
}

function cancelEditingSiteName() {
  isEditingSiteName.value = false
  editedSiteName.value = ''
}

// Device Manager FAB
function openDeviceManager(tab = 'groups') {
  deviceManagerTab.value = tab
  showDeviceManager.value = true
}

// Passkey authentication
const { getAuthConfig } = usePasskey()
const authConfig = ref({
  require_auth: false,
  passkey_supported: false
})

// Load auth config and current site on mount
onMounted(async () => {
  authConfig.value = await getAuthConfig()

  // Check for site UUID in URL parameters
  const urlParams = new URLSearchParams(window.location.search)
  const siteUuid = urlParams.get('site')

  if (siteUuid) {
    try {
      await fetchSiteByUuid(siteUuid)
      showToast('success', `Loaded shared site: ${currentSite.value.name}`)
    } catch (err) {
      showToast('error', 'Failed to load shared site')
      loadCurrentSite()
    }
  } else {
    loadCurrentSite()
  }
})

// Track unracked panel state
const unrackedPanelExpanded = ref(false)
provide('unrackedPanelExpanded', unrackedPanelExpanded)

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

function handleAuthenticated(user) {
  logInfo('User authenticated:', user)
}

// Share current site
function shareCurrentSite() {
  if (!currentSite.value || !currentSite.value.uuid) {
    showToast('error', 'No site loaded to share')
    return
  }

  const shareUrl = `${window.location.origin}?site=${currentSite.value.uuid}`

  // Copy to clipboard
  navigator.clipboard.writeText(shareUrl).then(() => {
    showToast('success', 'Share link copied to clipboard!')
  }).catch(err => {
    logError('Failed to copy', err)
    showToast('error', 'Failed to copy link')
  })
}

// Navigate to documentation
function navigateToDocs() {
  window.location.href = '/docs/'
}

function navigateToApiDocs() {
  window.location.href = '/api/docs/'
}
</script>