<template>
  <div
    v-if="visible"
    class="fixed inset-0 flex items-center justify-center z-50 transition-opacity duration-200"
    style="background-color: rgba(0, 0, 0, 0.3); backdrop-filter: blur(4px);"
    @click.self="close"
  >
    <div class="rounded-xl shadow-2xl w-full max-w-xl transform transition-all duration-200" style="background-color: var(--bg-primary);">
      <div class="flex items-center justify-between mb-6 p-6 rounded-t-xl" style="background-color: var(--color-primary);">
        <h2 class="text-2xl font-bold" style="color: #0c0c0d;">
          {{ mode === 'save' ? 'Save Rack Configuration' : 'Load Rack Configuration' }}
        </h2>
        <button
          @click="close"
          class="transition-colors"
          style="color: rgba(12, 12, 13, 0.7);"
          @mouseover="$event.target.style.color = '#0c0c0d'"
          @mouseout="$event.target.style.color = 'rgba(12, 12, 13, 0.7)'"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="px-6 pb-6">
        <!-- Error Display -->
        <div v-if="error" class="mb-4 p-3 rounded" style="background-color: #fee2e2; border: 1px solid #fecaca; color: #991b1b;">
          <div class="flex items-center justify-between">
            <span>{{ error }}</span>
            <button @click="error = null" style="color: #991b1b;">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Site Selection/Creation -->
        <div class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            Site
          </label>

          <div class="flex gap-2">
            <div class="flex-1 relative">
              <select
                v-model="selectedSite"
                class="w-full px-3 py-2 rounded focus:outline-none transition-colors appearance-none"
                style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
                @focus="$event.target.style.borderColor = 'var(--color-primary)'; $event.target.style.boxShadow = '0 0 0 2px rgba(132, 204, 22, 0.2)'"
                @blur="$event.target.style.borderColor = 'var(--border-color)'; $event.target.style.boxShadow = 'none'"
                :disabled="loading"
              >
                <option :value="null">Select a site</option>
                <option v-for="site in sites" :key="site.id" :value="site">
                  {{ site.name }}
                </option>
              </select>
              <div class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none" style="color: var(--text-secondary);">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>

            <button
              @click="showNewSiteDialog = true"
              class="px-4 py-2 rounded transition-colors"
              style="background-color: var(--bg-secondary); color: var(--text-primary); border: 1px solid var(--border-color);"
              @mouseover="$event.target.style.backgroundColor = 'var(--color-primary-light)'"
              @mouseout="$event.target.style.backgroundColor = 'var(--bg-secondary)'"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Save Mode: Rack Name Input -->
        <div v-if="mode === 'save'" class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            Rack Configuration Name
          </label>
          <input
            v-model="rackName"
            type="text"
            placeholder="Enter configuration name (e.g., Production Rack)"
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
            @focus="$event.target.style.borderColor = 'var(--color-primary)'; $event.target.style.boxShadow = '0 0 0 2px rgba(132, 204, 22, 0.2)'"
            @blur="$event.target.style.borderColor = 'var(--border-color)'; $event.target.style.boxShadow = 'none'"
          />
        </div>

        <!-- Save Mode: Description -->
        <div v-if="mode === 'save'" class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            Description (Optional)
          </label>
          <textarea
            v-model="description"
            placeholder="Enter description"
            rows="3"
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors resize-none"
            style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
            @focus="$event.target.style.borderColor = 'var(--color-primary)'; $event.target.style.boxShadow = '0 0 0 2px rgba(132, 204, 22, 0.2)'"
            @blur="$event.target.style.borderColor = 'var(--border-color)'; $event.target.style.boxShadow = 'none'"
          ></textarea>
        </div>

        <!-- Load Mode: Rack Configuration Selection -->
        <div v-if="mode === 'load' && selectedSite" class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            Rack Configuration
          </label>

          <div class="rounded-lg overflow-hidden" style="border: 1px solid var(--border-color);">
            <div
              v-if="loadingRacks"
              class="p-4 text-center"
              style="color: var(--text-secondary);"
            >
              <svg class="w-5 h-5 inline animate-spin mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Loading configurations...
            </div>

            <div
              v-else-if="!availableRacks || availableRacks.length === 0"
              class="p-4 text-center"
              style="color: var(--text-secondary);"
            >
              No saved configurations for this site.
            </div>

            <div v-else class="divide-y" style="border-color: var(--border-color);">
              <div
                v-for="rack in availableRacks"
                :key="rack.id"
                class="p-3 cursor-pointer flex justify-between items-start transition-colors"
                :style="{
                  backgroundColor: selectedRack?.id === rack.id ? 'rgba(132, 204, 22, 0.1)' : 'transparent'
                }"
                @click="selectedRack = rack"
                @mouseover="handleRackHover($event, rack, true)"
                @mouseout="handleRackHover($event, rack, false)"
              >
                <div class="flex-1">
                  <div class="font-medium" style="color: var(--text-primary);">{{ rack.name }}</div>
                  <div v-if="rack.description" class="text-sm mt-1" style="color: var(--text-secondary);">
                    {{ rack.description }}
                  </div>
                  <div class="text-xs mt-1" style="color: var(--text-secondary);">
                    Updated: {{ formatDate(rack.updated_at) }}
                  </div>
                </div>

                <button
                  @click.stop="confirmDelete(rack)"
                  class="p-2 rounded transition-colors"
                  style="color: #ef4444;"
                  @mouseover="$event.target.style.backgroundColor = 'rgba(239, 68, 68, 0.1)'"
                  @mouseout="$event.target.style.backgroundColor = 'transparent'"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Buttons -->
        <div class="flex gap-2 mt-6">
          <button
            @click="close"
            class="flex-1 px-4 py-2 rounded transition-opacity"
            style="background-color: var(--color-primary-light); color: var(--color-primary-dark);"
            @mouseover="$event.target.style.opacity = '0.8'"
            @mouseout="$event.target.style.opacity = '1'"
          >
            Cancel
          </button>

          <button
            v-if="mode === 'save'"
            @click="handleSave"
            :disabled="!canSave || saving"
            class="flex-1 px-4 py-2 text-white rounded transition-colors"
            :style="{
              backgroundColor: (!canSave || saving) ? 'var(--color-primary-light)' : 'var(--color-primary)',
              opacity: (!canSave || saving) ? '0.5' : '1',
              cursor: (!canSave || saving) ? 'not-allowed' : 'pointer'
            }"
            @mouseover="handleSaveButtonHover($event, true)"
            @mouseout="handleSaveButtonHover($event, false)"
          >
            <span v-if="saving">
              <svg class="w-4 h-4 inline animate-spin mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Saving...
            </span>
            <span v-else>Save</span>
          </button>

          <button
            v-if="mode === 'load'"
            @click="handleLoad"
            :disabled="!selectedRack || loading"
            class="flex-1 px-4 py-2 text-white rounded transition-colors"
            :style="{
              backgroundColor: (!selectedRack || loading) ? 'var(--color-primary-light)' : 'var(--color-primary)',
              opacity: (!selectedRack || loading) ? '0.5' : '1',
              cursor: (!selectedRack || loading) ? 'not-allowed' : 'pointer'
            }"
            @mouseover="handleLoadButtonHover($event, true)"
            @mouseout="handleLoadButtonHover($event, false)"
          >
            <span v-if="loading">
              <svg class="w-4 h-4 inline animate-spin mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Loading...
            </span>
            <span v-else>Load</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- New Site Dialog -->
  <div
    v-if="showNewSiteDialog"
    class="fixed inset-0 flex items-center justify-center z-50 transition-opacity duration-200"
    style="background-color: rgba(0, 0, 0, 0.3); backdrop-filter: blur(4px);"
    @click.self="showNewSiteDialog = false"
  >
    <div class="rounded-xl shadow-2xl w-full max-w-md transform transition-all duration-200" style="background-color: var(--bg-primary);">
      <div class="flex items-center justify-between mb-6 p-6 rounded-t-xl" style="background-color: var(--color-primary);">
        <h2 class="text-2xl font-bold" style="color: #0c0c0d;">Create New Site</h2>
        <button
          @click="showNewSiteDialog = false"
          class="transition-colors"
          style="color: rgba(12, 12, 13, 0.7);"
          @mouseover="$event.target.style.color = '#0c0c0d'"
          @mouseout="$event.target.style.color = 'rgba(12, 12, 13, 0.7)'"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="px-6 pb-6">
        <div class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            Site Name
          </label>
          <input
            v-model="newSiteName"
            type="text"
            placeholder="Enter site name"
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
            @focus="$event.target.style.borderColor = 'var(--color-primary)'; $event.target.style.boxShadow = '0 0 0 2px rgba(132, 204, 22, 0.2)'"
            @blur="$event.target.style.borderColor = 'var(--border-color)'; $event.target.style.boxShadow = 'none'"
          />
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            Description (Optional)
          </label>
          <textarea
            v-model="newSiteDescription"
            placeholder="Enter description"
            rows="3"
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors resize-none"
            style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
            @focus="$event.target.style.borderColor = 'var(--color-primary)'; $event.target.style.boxShadow = '0 0 0 2px rgba(132, 204, 22, 0.2)'"
            @blur="$event.target.style.borderColor = 'var(--border-color)'; $event.target.style.boxShadow = 'none'"
          ></textarea>
        </div>

        <div class="flex gap-2 mt-6">
          <button
            @click="showNewSiteDialog = false"
            class="flex-1 px-4 py-2 rounded transition-opacity"
            style="background-color: var(--color-primary-light); color: var(--color-primary-dark);"
            @mouseover="$event.target.style.opacity = '0.8'"
            @mouseout="$event.target.style.opacity = '1'"
          >
            Cancel
          </button>

          <button
            @click="handleCreateSite"
            :disabled="!newSiteName?.trim() || creating"
            class="flex-1 px-4 py-2 text-white rounded transition-colors"
            :style="{
              backgroundColor: (!newSiteName?.trim() || creating) ? 'var(--color-primary-light)' : 'var(--color-primary)',
              opacity: (!newSiteName?.trim() || creating) ? '0.5' : '1',
              cursor: (!newSiteName?.trim() || creating) ? 'not-allowed' : 'pointer'
            }"
            @mouseover="handleCreateSiteButtonHover($event, true)"
            @mouseout="handleCreateSiteButtonHover($event, false)"
          >
            <span v-if="creating">
              <svg class="w-4 h-4 inline animate-spin mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Creating...
            </span>
            <span v-else>Create</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useDatabase } from '../composables/useDatabase';
import { useToast } from '../composables/useToast';

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  mode: {
    type: String,
    default: 'save', // 'save' or 'load'
    validator: (value) => ['save', 'load'].includes(value)
  },
  currentConfig: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['update:modelValue', 'configLoaded']);

const {
  loading,
  error,
  sites,
  currentSite,
  fetchSites,
  createSite,
  setCurrentSite,
  setCurrentRackName,
  saveRackConfiguration,
  loadRacksBySite,
  loadRackConfiguration,
  deleteRackConfiguration
} = useDatabase();

const { showToast } = useToast();

// Dialog state
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

// Site management
const selectedSite = ref(null);
const showNewSiteDialog = ref(false);
const newSiteName = ref('');
const newSiteDescription = ref('');
const creating = ref(false);

// Rack management
const rackName = ref('');
const description = ref('');
const selectedRack = ref(null);
const availableRacks = ref([]);
const loadingRacks = ref(false);
const saving = ref(false);

// Load sites when dialog opens
watch(visible, async (isVisible) => {
  if (isVisible) {
    try {
      await fetchSites();
      // Set current site if available
      if (currentSite.value) {
        selectedSite.value = sites.value.find(s => s.id === currentSite.value.id) || null;
      }
    } catch (err) {
      error.value = 'Failed to load sites';
    }
  } else {
    // Reset form when closing
    resetForm();
  }
});

// Load racks when site is selected
watch(selectedSite, async (site) => {
  if (site && props.mode === 'load') {
    loadingRacks.value = true;
    try {
      availableRacks.value = await loadRacksBySite(site.id);
    } catch (err) {
      error.value = 'Failed to load rack configurations';
    } finally {
      loadingRacks.value = false;
    }
  }
});

// Computed
const canSave = computed(() => {
  return selectedSite.value && rackName.value?.trim().length > 0;
});

// Methods
function resetForm() {
  rackName.value = '';
  description.value = '';
  selectedRack.value = null;
  availableRacks.value = [];
  error.value = null;
}

function close() {
  visible.value = false;
}

async function handleCreateSite() {
  if (!newSiteName.value?.trim()) return;

  creating.value = true;
  error.value = null;

  try {
    const site = await createSite(newSiteName.value.trim(), newSiteDescription.value?.trim() || null);
    selectedSite.value = site;
    setCurrentSite(site);
    showNewSiteDialog.value = false;
    newSiteName.value = '';
    newSiteDescription.value = '';
    showToast('success', 'Site created successfully');
  } catch (err) {
    error.value = err.message;
  } finally {
    creating.value = false;
  }
}

async function handleSave() {
  if (!canSave.value) return;

  saving.value = true;
  error.value = null;

  try {
    await saveRackConfiguration(
      selectedSite.value.id,
      rackName.value.trim(),
      props.currentConfig,
      description.value?.trim() || null
    );

    setCurrentSite(selectedSite.value);
    setCurrentRackName(rackName.value.trim()); // Set rack name for auto-save
    showToast('success', `Rack configuration "${rackName.value}" saved successfully`);
    close();
  } catch (err) {
    error.value = err.message;
  } finally {
    saving.value = false;
  }
}

async function handleLoad() {
  if (!selectedRack.value) return;

  try {
    const rack = await loadRackConfiguration(selectedSite.value.id, selectedRack.value.name);

    if (rack && rack.config_data) {
      setCurrentSite(selectedSite.value);
      setCurrentRackName(rack.name); // Set rack name for auto-save
      emit('configLoaded', rack.config_data);
      showToast('success', `Loaded "${rack.name}"`);
      close();
    }
  } catch (err) {
    error.value = err.message;
  }
}

async function confirmDelete(rack) {
  if (!confirm(`Are you sure you want to delete "${rack.name}"?`)) {
    return;
  }

  try {
    await deleteRackConfiguration(rack.id);
    availableRacks.value = availableRacks.value.filter(r => r.id !== rack.id);
    showToast('success', 'Configuration deleted');
  } catch (err) {
    error.value = err.message;
  }
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleString();
}

function handleRackHover(event, rack, isHovering) {
  if (selectedRack.value?.id === rack.id) return;
  event.currentTarget.style.backgroundColor = isHovering ? 'var(--bg-secondary)' : 'transparent';
}

function handleSaveButtonHover(event, isHovering) {
  if (!canSave.value || saving.value) return;
  event.target.style.backgroundColor = isHovering ? 'var(--color-primary-dark)' : 'var(--color-primary)';
}

function handleLoadButtonHover(event, isHovering) {
  if (!selectedRack.value || loading.value) return;
  event.target.style.backgroundColor = isHovering ? 'var(--color-primary-dark)' : 'var(--color-primary)';
}

function handleCreateSiteButtonHover(event, isHovering) {
  if (!newSiteName.value?.trim() || creating.value) return;
  event.target.style.backgroundColor = isHovering ? 'var(--color-primary-dark)' : 'var(--color-primary)';
}
</script>

<style scoped>
/* Divide-y utility for borders between rack items */
.divide-y > * + * {
  border-top-width: 1px;
  border-color: var(--border-color);
}

/* Spinning animation for loading indicators */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>
