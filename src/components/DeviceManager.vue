<template>
  <div
    class="fixed inset-0 flex items-center justify-center z-50 transition-opacity duration-200"
    style="background-color: rgba(0, 0, 0, 0.3); backdrop-filter: blur(4px);"
    @click.self="$emit('close')"
  >
    <div class="rounded-xl shadow-2xl w-full max-w-4xl transform transition-all duration-200" style="background-color: var(--bg-primary); max-height: 90vh; display: flex; flex-direction: column;">
      <div class="flex items-center justify-between mb-6 p-6 rounded-t-xl" style="background-color: var(--color-primary);">
        <h2 class="text-2xl font-bold" style="color: #0c0c0d;">Manage Devices & Groups</h2>
        <button
          @click="$emit('close')"
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

      <div class="px-6 pb-6 flex-1 overflow-hidden flex flex-col">
        <!-- Tab Navigation -->
        <div class="flex gap-2 mb-6">
          <button
            @click="activeTab = 'groups'"
            class="px-4 py-2 rounded transition-colors font-medium"
            :style="{
              backgroundColor: activeTab === 'groups' ? 'var(--color-primary)' : 'var(--bg-secondary)',
              color: activeTab === 'groups' ? '#0c0c0d' : 'var(--text-primary)'
            }"
          >
            Device Groups
          </button>
          <button
            @click="activeTab = 'devices'"
            class="px-4 py-2 rounded transition-colors font-medium"
            :style="{
              backgroundColor: activeTab === 'devices' ? 'var(--color-primary)' : 'var(--bg-secondary)',
              color: activeTab === 'devices' ? '#0c0c0d' : 'var(--text-primary)'
            }"
          >
            Devices
          </button>
        </div>

        <!-- Device Groups Tab -->
        <div v-if="activeTab === 'groups'" class="flex-1 overflow-y-auto">
          <div class="mb-4">
            <button
              @click="showAddGroupDialog = true"
              class="px-4 py-2 rounded transition-colors font-medium text-white"
              style="background-color: var(--color-primary);"
              @mouseover="$event.target.style.backgroundColor = 'var(--color-primary-dark)'"
              @mouseout="$event.target.style.backgroundColor = 'var(--color-primary)'"
            >
              Add Device Group
            </button>
          </div>

          <div class="space-y-2">
            <div
              v-for="group in deviceGroups"
              :key="group.id"
              class="p-4 rounded border flex items-center justify-between"
              style="background-color: var(--bg-secondary); border-color: var(--border-color);"
            >
              <div class="flex items-center gap-4">
                <div
                  class="w-12 h-12 rounded"
                  :style="{ backgroundColor: group.color }"
                ></div>
                <div>
                  <div class="font-medium" style="color: var(--text-primary);">{{ group.name }}</div>
                  <div class="text-sm" style="color: var(--text-secondary);">{{ group.deviceCount || 0 }} devices</div>
                </div>
              </div>
              <button
                @click="deleteGroup(group.id)"
                class="p-2 rounded transition-colors"
                style="color: #ef4444;"
                @mouseover="$event.target.style.backgroundColor = 'rgba(239, 68, 68, 0.1)'"
                @mouseout="$event.target.style.backgroundColor = 'transparent'"
                title="Delete group"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Devices Tab -->
        <div v-if="activeTab === 'devices'" class="flex-1 overflow-y-auto">
          <div class="mb-4">
            <button
              @click="showAddDeviceDialog = true"
              class="px-4 py-2 rounded transition-colors font-medium text-white"
              style="background-color: var(--color-primary);"
              @mouseover="$event.target.style.backgroundColor = 'var(--color-primary-dark)'"
              @mouseout="$event.target.style.backgroundColor = 'var(--color-primary)'"
            >
              Add Device
            </button>
          </div>

          <div class="space-y-2">
            <div
              v-for="device in customDevices"
              :key="device.id"
              class="p-4 rounded border flex items-center justify-between"
              style="background-color: var(--bg-secondary); border-color: var(--border-color);"
            >
              <div class="flex items-center gap-4">
                <div
                  class="w-12 h-12 rounded flex items-center justify-center text-white font-bold"
                  :style="{ backgroundColor: device.color }"
                >
                  {{ device.ruSize }}U
                </div>
                <div>
                  <div class="font-medium" style="color: var(--text-primary);">{{ device.name }}</div>
                  <div class="text-sm" style="color: var(--text-secondary);">
                    {{ device.category }} • {{ device.ruSize }}U • {{ device.powerDraw }}W
                  </div>
                  <div v-if="device.description" class="text-xs mt-1" style="color: var(--text-secondary);">
                    {{ device.description }}
                  </div>
                </div>
              </div>
              <button
                @click="deleteDevice(device.id)"
                class="p-2 rounded transition-colors"
                style="color: #ef4444;"
                @mouseover="$event.target.style.backgroundColor = 'rgba(239, 68, 68, 0.1)'"
                @mouseout="$event.target.style.backgroundColor = 'transparent'"
                title="Delete device"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Add Device Group Dialog -->
  <div
    v-if="showAddGroupDialog"
    class="fixed inset-0 flex items-center justify-center z-50 transition-opacity duration-200"
    style="background-color: rgba(0, 0, 0, 0.3); backdrop-filter: blur(4px);"
    @click.self="showAddGroupDialog = false"
  >
    <div class="rounded-xl shadow-2xl w-full max-w-md transform transition-all duration-200" style="background-color: var(--bg-primary);">
      <div class="flex items-center justify-between mb-6 p-6 rounded-t-xl" style="background-color: var(--color-primary);">
        <h2 class="text-2xl font-bold" style="color: #0c0c0d;">Add Device Group</h2>
        <button
          @click="showAddGroupDialog = false"
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
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">Group Name</label>
          <input
            v-model="newGroup.name"
            type="text"
            placeholder="e.g., Servers, Storage, Network"
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
          />
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">Default Color</label>
          <div class="flex gap-2 items-center">
            <input
              v-model="newGroup.color"
              type="color"
              class="w-16 h-10 rounded cursor-pointer"
            />
            <input
              v-model="newGroup.color"
              type="text"
              placeholder="#4A90E2"
              class="flex-1 px-3 py-2 rounded focus:outline-none transition-colors"
              style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
            />
          </div>
        </div>

        <div class="flex gap-2">
          <button
            @click="showAddGroupDialog = false"
            class="flex-1 px-4 py-2 rounded transition-colors"
            style="background-color: var(--bg-secondary); color: var(--text-primary);"
            @mouseover="$event.target.style.backgroundColor = 'var(--border-color)'"
            @mouseout="$event.target.style.backgroundColor = 'var(--bg-secondary)'"
          >
            Cancel
          </button>
          <button
            @click="handleAddGroup"
            :disabled="!newGroup.name?.trim()"
            class="flex-1 px-4 py-2 text-white rounded transition-colors"
            :style="{
              backgroundColor: !newGroup.name?.trim() ? 'var(--color-primary-light)' : 'var(--color-primary)',
              opacity: !newGroup.name?.trim() ? '0.5' : '1',
              cursor: !newGroup.name?.trim() ? 'not-allowed' : 'pointer'
            }"
          >
            Add Group
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Add Device Dialog -->
  <div
    v-if="showAddDeviceDialog"
    class="fixed inset-0 flex items-center justify-center z-50 transition-opacity duration-200"
    style="background-color: rgba(0, 0, 0, 0.3); backdrop-filter: blur(4px);"
    @click.self="showAddDeviceDialog = false"
  >
    <div class="rounded-xl shadow-2xl w-full max-w-md transform transition-all duration-200" style="background-color: var(--bg-primary);">
      <div class="flex items-center justify-between mb-6 p-6 rounded-t-xl" style="background-color: var(--color-primary);">
        <h2 class="text-2xl font-bold" style="color: #0c0c0d;">Add Device</h2>
        <button
          @click="showAddDeviceDialog = false"
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

      <div class="px-6 pb-6" style="max-height: 70vh; overflow-y: auto;">
        <div class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">Device Model Name</label>
          <input
            v-model="newDevice.name"
            type="text"
            placeholder="e.g., Dell PowerEdge R750"
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
          />
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">Device Group</label>
          <select
            v-model="newDevice.category"
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
          >
            <option value="">Select a group...</option>
            <option v-for="group in deviceGroups" :key="group.id" :value="group.name">
              {{ group.name }}
            </option>
          </select>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">RU Size (Rack Units)</label>
          <input
            v-model.number="newDevice.ruSize"
            type="number"
            min="1"
            max="42"
            placeholder="e.g., 2"
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
          />
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">Power Draw (Watts)</label>
          <input
            v-model.number="newDevice.powerDraw"
            type="number"
            min="0"
            placeholder="e.g., 750"
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
          />
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">Color</label>
          <div class="flex gap-2 items-center">
            <input
              v-model="newDevice.color"
              type="color"
              class="w-16 h-10 rounded cursor-pointer"
            />
            <input
              v-model="newDevice.color"
              type="text"
              placeholder="#4A90E2"
              class="flex-1 px-3 py-2 rounded focus:outline-none transition-colors"
              style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
            />
          </div>
          <p class="text-xs mt-1" style="color: var(--text-secondary);">
            Uses group default color if not specified
          </p>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">Description (Optional)</label>
          <textarea
            v-model="newDevice.description"
            rows="3"
            placeholder="Additional details about this device..."
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
          ></textarea>
        </div>

        <div class="flex gap-2">
          <button
            @click="showAddDeviceDialog = false"
            class="flex-1 px-4 py-2 rounded transition-colors"
            style="background-color: var(--bg-secondary); color: var(--text-primary);"
            @mouseover="$event.target.style.backgroundColor = 'var(--border-color)'"
            @mouseout="$event.target.style.backgroundColor = 'var(--bg-secondary)'"
          >
            Cancel
          </button>
          <button
            @click="handleAddDevice"
            :disabled="!canAddDevice"
            class="flex-1 px-4 py-2 text-white rounded transition-colors"
            :style="{
              backgroundColor: !canAddDevice ? 'var(--color-primary-light)' : 'var(--color-primary)',
              opacity: !canAddDevice ? '0.5' : '1',
              cursor: !canAddDevice ? 'not-allowed' : 'pointer'
            }"
          >
            Add Device
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useToast } from '../composables/useToast';

const { showToast } = useToast();

const activeTab = ref('groups');
const showAddGroupDialog = ref(false);
const showAddDeviceDialog = ref(false);

const deviceGroups = ref([]);
const customDevices = ref([]);

const newGroup = ref({
  name: '',
  color: '#4A90E2'
});

const newDevice = ref({
  name: '',
  category: '',
  ruSize: 1,
  powerDraw: 0,
  color: '',
  description: ''
});

const canAddDevice = computed(() => {
  return newDevice.value.name?.trim() &&
         newDevice.value.category &&
         newDevice.value.ruSize > 0 &&
         newDevice.value.powerDraw >= 0;
});

onMounted(() => {
  loadDeviceGroups();
  loadCustomDevices();
});

function loadDeviceGroups() {
  const saved = localStorage.getItem('racksum-device-groups');
  if (saved) {
    try {
      deviceGroups.value = JSON.parse(saved);
    } catch (err) {
      console.error('Error loading device groups:', err);
    }
  }
}

function loadCustomDevices() {
  const saved = localStorage.getItem('racksum-custom-devices');
  if (saved) {
    try {
      customDevices.value = JSON.parse(saved);
    } catch (err) {
      console.error('Error loading custom devices:', err);
    }
  }
}

function saveDeviceGroups() {
  localStorage.setItem('racksum-device-groups', JSON.stringify(deviceGroups.value));
}

function saveCustomDevices() {
  localStorage.setItem('racksum-custom-devices', JSON.stringify(customDevices.value));
}

function handleAddGroup() {
  if (!newGroup.value.name?.trim()) return;

  const group = {
    id: `group-${Date.now()}`,
    name: newGroup.value.name.trim(),
    color: newGroup.value.color,
    deviceCount: 0
  };

  deviceGroups.value.push(group);
  saveDeviceGroups();

  showToast('success', 'Device group added');

  newGroup.value = {
    name: '',
    color: '#4A90E2'
  };
  showAddGroupDialog.value = false;
}

function deleteGroup(groupId) {
  const group = deviceGroups.value.find(g => g.id === groupId);
  if (!confirm(`Delete device group "${group.name}"? Devices in this group will not be deleted.`)) {
    return;
  }

  deviceGroups.value = deviceGroups.value.filter(g => g.id !== groupId);
  saveDeviceGroups();
  showToast('success', 'Device group deleted');
}

function handleAddDevice() {
  if (!canAddDevice.value) return;

  // Get color from group if not specified
  let color = newDevice.value.color;
  if (!color) {
    const group = deviceGroups.value.find(g => g.name === newDevice.value.category);
    color = group?.color || '#4A90E2';
  }

  const device = {
    id: `device-${Date.now()}`,
    name: newDevice.value.name.trim(),
    category: newDevice.value.category,
    ruSize: newDevice.value.ruSize,
    powerDraw: newDevice.value.powerDraw,
    color: color,
    description: newDevice.value.description?.trim() || '',
    custom: true
  };

  customDevices.value.push(device);
  saveCustomDevices();

  // Update group device count
  updateGroupCounts();

  showToast('success', 'Device added');

  newDevice.value = {
    name: '',
    category: '',
    ruSize: 1,
    powerDraw: 0,
    color: '',
    description: ''
  };
  showAddDeviceDialog.value = false;

  // Emit event to notify parent to reload devices
  window.dispatchEvent(new CustomEvent('devices-updated'));
}

function deleteDevice(deviceId) {
  const device = customDevices.value.find(d => d.id === deviceId);
  if (!confirm(`Delete device "${device.name}"?`)) {
    return;
  }

  customDevices.value = customDevices.value.filter(d => d.id !== deviceId);
  saveCustomDevices();
  updateGroupCounts();
  showToast('success', 'Device deleted');

  // Emit event to notify parent to reload devices
  window.dispatchEvent(new CustomEvent('devices-updated'));
}

function updateGroupCounts() {
  deviceGroups.value.forEach(group => {
    group.deviceCount = customDevices.value.filter(d => d.category === group.name).length;
  });
  saveDeviceGroups();
}
</script>
