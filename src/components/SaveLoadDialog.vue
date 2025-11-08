<template>
  <Dialog
    v-model:visible="visible"
    modal
    :header="mode === 'save' ? 'Save Rack Configuration' : 'Load Rack Configuration'"
    :style="{ width: '600px' }"
    :closable="true"
  >
    <div class="space-y-4">
      <!-- Error display -->
      <Message v-if="error" severity="error" @close="error = null">
        {{ error }}
      </Message>

      <!-- Site Selection/Creation -->
      <div class="space-y-2">
        <label class="block text-sm font-medium">Site</label>

        <div class="flex gap-2">
          <Dropdown
            v-model="selectedSite"
            :options="sites"
            option-label="name"
            placeholder="Select a site"
            class="flex-1"
            :loading="loading"
          >
            <template #value="slotProps">
              <div v-if="slotProps.value">{{ slotProps.value.name }}</div>
              <span v-else>{{ slotProps.placeholder }}</span>
            </template>
          </Dropdown>

          <Button
            label="New Site"
            icon="pi pi-plus"
            @click="showNewSiteDialog = true"
            severity="secondary"
            outlined
          />
        </div>
      </div>

      <!-- Save Mode: Rack Name Input -->
      <div v-if="mode === 'save'" class="space-y-2">
        <label class="block text-sm font-medium">Rack Configuration Name</label>
        <InputText
          v-model="rackName"
          placeholder="Enter configuration name (e.g., Production Rack)"
          class="w-full"
        />
      </div>

      <!-- Save Mode: Description -->
      <div v="mode === 'save'" class="space-y-2">
        <label class="block text-sm font-medium">Description (Optional)</label>
        <Textarea
          v-model="description"
          placeholder="Enter description"
          rows="3"
          class="w-full"
        />
      </div>

      <!-- Load Mode: Rack Configuration Selection -->
      <div v-if="mode === 'load' && selectedSite" class="space-y-2">
        <label class="block text-sm font-medium">Rack Configuration</label>

        <div class="border rounded-lg overflow-hidden">
          <div
            v-if="loadingRacks"
            class="p-4 text-center text-gray-500"
          >
            <i class="pi pi-spin pi-spinner mr-2"></i>
            Loading configurations...
          </div>

          <div
            v-else-if="!availableRacks || availableRacks.length === 0"
            class="p-4 text-center text-gray-500"
          >
            No saved configurations for this site.
          </div>

          <div v-else class="divide-y">
            <div
              v-for="rack in availableRacks"
              :key="rack.id"
              class="p-3 hover:bg-gray-50 cursor-pointer flex justify-between items-start"
              :class="{ 'bg-blue-50': selectedRack?.id === rack.id }"
              @click="selectedRack = rack"
            >
              <div class="flex-1">
                <div class="font-medium">{{ rack.name }}</div>
                <div v-if="rack.description" class="text-sm text-gray-600 mt-1">
                  {{ rack.description }}
                </div>
                <div class="text-xs text-gray-500 mt-1">
                  Updated: {{ formatDate(rack.updated_at) }}
                </div>
              </div>

              <Button
                icon="pi pi-trash"
                severity="danger"
                text
                rounded
                size="small"
                @click.stop="confirmDelete(rack)"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <Button
        label="Cancel"
        severity="secondary"
        @click="close"
        outlined
      />
      <Button
        v-if="mode === 'save'"
        label="Save"
        icon="pi pi-save"
        @click="handleSave"
        :loading="saving"
        :disabled="!canSave"
      />
      <Button
        v-if="mode === 'load'"
        label="Load"
        icon="pi pi-download"
        @click="handleLoad"
        :loading="loading"
        :disabled="!selectedRack"
      />
    </template>
  </Dialog>

  <!-- New Site Dialog -->
  <Dialog
    v-model:visible="showNewSiteDialog"
    modal
    header="Create New Site"
    :style="{ width: '400px' }"
  >
    <div class="space-y-4">
      <div class="space-y-2">
        <label class="block text-sm font-medium">Site Name</label>
        <InputText
          v-model="newSiteName"
          placeholder="Enter site name"
          class="w-full"
        />
      </div>

      <div class="space-y-2">
        <label class="block text-sm font-medium">Description (Optional)</label>
        <Textarea
          v-model="newSiteDescription"
          placeholder="Enter description"
          rows="3"
          class="w-full"
        />
      </div>
    </div>

    <template #footer>
      <Button
        label="Cancel"
        severity="secondary"
        @click="showNewSiteDialog = false"
        outlined
      />
      <Button
        label="Create"
        icon="pi pi-plus"
        @click="handleCreateSite"
        :loading="creating"
        :disabled="!newSiteName?.trim()"
      />
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import Dropdown from 'primevue/dropdown';
import Message from 'primevue/message';
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
</script>

<style scoped>
.space-y-2 > * + * {
  margin-top: 0.5rem;
}

.space-y-4 > * + * {
  margin-top: 1rem;
}
</style>
