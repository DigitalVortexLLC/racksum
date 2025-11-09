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
          @mouseover="$event.currentTarget.style.color = '#0c0c0d'"
          @mouseout="$event.currentTarget.style.color = 'rgba(12, 12, 13, 0.7)'"
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
          <button
            @click="activeTab = 'providers'"
            class="px-4 py-2 rounded transition-colors font-medium"
            :style="{
              backgroundColor: activeTab === 'providers' ? 'var(--color-primary)' : 'var(--bg-secondary)',
              color: activeTab === 'providers' ? '#0c0c0d' : 'var(--text-primary)'
            }"
          >
            Resource Providers
          </button>
          <button
            @click="activeTab = 'import-export'"
            class="px-4 py-2 rounded transition-colors font-medium"
            :style="{
              backgroundColor: activeTab === 'import-export' ? 'var(--color-primary)' : 'var(--bg-secondary)',
              color: activeTab === 'import-export' ? '#0c0c0d' : 'var(--text-primary)'
            }"
          >
            Import/Export
          </button>
        </div>

        <!-- Device Groups Tab -->
        <div v-if="activeTab === 'groups'" class="flex-1 overflow-y-auto">
          <div class="mb-4">
            <button
              @click="showAddGroupDialog = true"
              class="px-4 py-2 rounded transition-colors font-medium text-white"
              style="background-color: var(--color-primary);"
              @mouseover="$event.currentTarget.style.backgroundColor = 'var(--color-primary-dark)'"
              @mouseout="$event.currentTarget.style.backgroundColor = 'var(--color-primary)'"
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
              <div class="flex gap-2">
                <button
                  @click="editGroup(group)"
                  class="p-2 rounded transition-colors"
                  style="color: var(--color-primary);"
                  @mouseover="$event.currentTarget.style.backgroundColor = 'rgba(74, 144, 226, 0.1)'"
                  @mouseout="$event.currentTarget.style.backgroundColor = 'transparent'"
                  title="Edit group"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
                <button
                  @click="deleteGroup(group.id)"
                  class="p-2 rounded transition-colors"
                  style="color: #ef4444;"
                  @mouseover="$event.currentTarget.style.backgroundColor = 'rgba(239, 68, 68, 0.1)'"
                  @mouseout="$event.currentTarget.style.backgroundColor = 'transparent'"
                  title="Delete group"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
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
              @mouseover="$event.currentTarget.style.backgroundColor = 'var(--color-primary-dark)'"
              @mouseout="$event.currentTarget.style.backgroundColor = 'var(--color-primary)'"
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
                    {{ device.category }} • {{ device.ruSize }}U • {{ device.powerDraw }}W • {{ device.powerPortsUsed || 1 }} port(s)
                  </div>
                  <div v-if="device.description" class="text-xs mt-1" style="color: var(--text-secondary);">
                    {{ device.description }}
                  </div>
                </div>
              </div>
              <div class="flex gap-2">
                <button
                  @click="duplicateDevice(device)"
                  class="p-2 rounded transition-colors"
                  style="color: var(--text-secondary);"
                  @mouseover="$event.currentTarget.style.backgroundColor = 'var(--border-color)'"
                  @mouseout="$event.currentTarget.style.backgroundColor = 'transparent'"
                  title="Duplicate device"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                </button>
                <button
                  @click="editDevice(device)"
                  class="p-2 rounded transition-colors"
                  style="color: var(--color-primary);"
                  @mouseover="$event.currentTarget.style.backgroundColor = 'rgba(74, 144, 226, 0.1)'"
                  @mouseout="$event.currentTarget.style.backgroundColor = 'transparent'"
                  title="Edit device"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
                <button
                  @click="deleteDevice(device.id)"
                  class="p-2 rounded transition-colors"
                  style="color: #ef4444;"
                  @mouseover="$event.currentTarget.style.backgroundColor = 'rgba(239, 68, 68, 0.1)'"
                  @mouseout="$event.currentTarget.style.backgroundColor = 'transparent'"
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

        <!-- Resource Providers Tab -->
        <div v-if="activeTab === 'providers'" class="flex-1 overflow-y-auto">
          <div class="mb-4 p-4 rounded border" style="background-color: rgba(74, 144, 226, 0.1); border-color: var(--color-primary);">
            <p class="text-sm" style="color: var(--text-primary);">
              <strong>Resource Providers</strong> are infrastructure components that add capacity to your site (PDUs, HVAC units, network uplinks, etc.). Define what provides power, cooling, and network resources instead of setting static totals.
            </p>
          </div>

          <div class="mb-4">
            <button
              @click="showAddProviderDialog = true"
              class="px-4 py-2 rounded transition-colors font-medium text-white"
              style="background-color: var(--color-primary);"
              @mouseover="$event.currentTarget.style.backgroundColor = 'var(--color-primary-dark)'"
              @mouseout="$event.currentTarget.style.backgroundColor = 'var(--color-primary)'"
            >
              Add Resource Provider
            </button>
          </div>

          <div class="space-y-2">
            <div
              v-for="provider in resourceProviders"
              :key="provider.id"
              class="p-4 rounded border flex items-center justify-between"
              style="background-color: var(--bg-secondary); border-color: var(--border-color);"
            >
              <div class="flex items-center gap-4 flex-1">
                <div class="flex flex-col items-center justify-center w-16 h-16 rounded" style="background-color: var(--border-color);">
                  <svg v-if="provider.type === 'power'" class="w-8 h-8" style="color: var(--color-primary);" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd" />
                  </svg>
                  <svg v-else-if="provider.type === 'cooling'" class="w-8 h-8" style="color: var(--color-primary);" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1.323l3.954 1.582 1.599-.8a1 1 0 01.894 1.79l-1.233.616 1.738 5.42a1 1 0 01-.285 1.05A3.989 3.989 0 0115 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.715-5.349L11 6.477V9a1 1 0 11-2 0V6.477L6.237 7.582l1.715 5.349a1 1 0 01-.285 1.05A3.989 3.989 0 015 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.738-5.42-1.233-.617a1 1 0 01.894-1.788l1.599.799L9 4.323V3a1 1 0 011-1zm-5 8.274l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L5 10.274zm10 0l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L15 10.274z" clip-rule="evenodd" />
                  </svg>
                  <svg v-else-if="provider.type === 'network'" class="w-8 h-8" style="color: var(--color-primary);" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
                  </svg>
                </div>
                <div class="flex-1">
                  <div class="font-medium" style="color: var(--text-primary);">{{ provider.name }}</div>
                  <div class="text-sm" style="color: var(--text-secondary);">
                    <span class="capitalize">{{ provider.type }}</span>
                    <span v-if="provider.powerCapacity > 0"> • {{ provider.powerCapacity }}W</span>
                    <span v-if="provider.powerPortsCapacity > 0"> • {{ provider.powerPortsCapacity }} ports</span>
                    <span v-if="provider.coolingCapacity > 0"> • {{ (provider.coolingCapacity / 12000).toFixed(1) }} Tons</span>
                    <span v-if="provider.networkCapacity > 0"> • {{ provider.networkCapacity }} Gbps</span>
                  </div>
                  <div v-if="provider.location" class="text-xs mt-1" style="color: var(--text-secondary);">
                    📍 {{ provider.location }}
                  </div>
                  <div v-if="provider.description" class="text-xs mt-1" style="color: var(--text-secondary);">
                    {{ provider.description }}
                  </div>
                </div>
              </div>
              <div class="flex gap-2">
                <button
                  @click="editProvider(provider)"
                  class="p-2 rounded transition-colors"
                  style="color: var(--color-primary);"
                  @mouseover="$event.currentTarget.style.backgroundColor = 'rgba(74, 144, 226, 0.1)'"
                  @mouseout="$event.currentTarget.style.backgroundColor = 'transparent'"
                  title="Edit provider"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
                <button
                  @click="deleteProvider(provider.id)"
                  class="p-2 rounded transition-colors"
                  style="color: #ef4444;"
                  @mouseover="$event.currentTarget.style.backgroundColor = 'rgba(239, 68, 68, 0.1)'"
                  @mouseout="$event.currentTarget.style.backgroundColor = 'transparent'"
                  title="Delete provider"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
            
            <div v-if="resourceProviders.length === 0" class="text-center py-8" style="color: var(--text-secondary);">
              No resource providers defined. Add providers to supply power, cooling, and network capacity.
            </div>
          </div>
        </div>

        <!-- Import/Export Tab -->
        <div v-if="activeTab === 'import-export'" class="flex-1 overflow-y-auto">
          <div class="space-y-6">
            <!-- Export Section -->
            <div class="p-6 rounded border" style="background-color: var(--bg-secondary); border-color: var(--border-color);">
              <h3 class="text-lg font-semibold mb-4" style="color: var(--text-primary);">
                Export Custom Devices
              </h3>
              <p class="text-sm mb-4" style="color: var(--text-secondary);">
                Download your custom device groups and devices as a JSON file. This file can be imported later or shared with others.
              </p>
              <div class="flex gap-2">
                <button
                  @click="exportDevices"
                  class="px-4 py-2 rounded transition-colors font-medium text-white"
                  style="background-color: var(--color-primary);"
                  @mouseover="$event.currentTarget.style.backgroundColor = 'var(--color-primary-dark)'"
                  @mouseout="$event.currentTarget.style.backgroundColor = 'var(--color-primary)'"
                >
                  <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  Export to JSON
                </button>
                <div class="flex-1 text-sm" style="color: var(--text-secondary); padding: 0.5rem 0;">
                  {{ deviceGroups.length }} groups, {{ customDevices.length }} devices
                </div>
              </div>
            </div>

            <!-- Import Section -->
            <div class="p-6 rounded border" style="background-color: var(--bg-secondary); border-color: var(--border-color);">
              <h3 class="text-lg font-semibold mb-4" style="color: var(--text-primary);">
                Import Custom Devices
              </h3>
              <p class="text-sm mb-4" style="color: var(--text-secondary);">
                Import device groups and devices from a JSON file. You can choose to merge with existing data or replace it completely.
              </p>
              
              <div class="mb-4">
                <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
                  Import Mode
                </label>
                <div class="flex gap-4">
                  <label class="flex items-center cursor-pointer">
                    <input
                      type="radio"
                      v-model="importMode"
                      value="merge"
                      class="mr-2"
                    />
                    <span class="text-sm" style="color: var(--text-primary);">
                      Merge (keep existing + add new)
                    </span>
                  </label>
                  <label class="flex items-center cursor-pointer">
                    <input
                      type="radio"
                      v-model="importMode"
                      value="replace"
                      class="mr-2"
                    />
                    <span class="text-sm" style="color: var(--text-primary);">
                      Replace (delete existing)
                    </span>
                  </label>
                </div>
              </div>

              <input
                ref="fileInput"
                type="file"
                accept=".json"
                class="hidden"
                @change="handleFileSelect"
              />
              <button
                @click="$refs.fileInput.click()"
                class="px-4 py-2 rounded transition-colors font-medium"
                style="background-color: var(--color-primary); color: #0c0c0d;"
                @mouseover="$event.currentTarget.style.backgroundColor = 'var(--color-primary-dark)'"
                @mouseout="$event.currentTarget.style.backgroundColor = 'var(--color-primary)'"
              >
                <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                Select JSON File
              </button>
              
              <div v-if="importError" class="mt-4 p-3 rounded" style="background-color: rgba(239, 68, 68, 0.1); color: #ef4444;">
                <p class="text-sm">{{ importError }}</p>
              </div>
            </div>

            <!-- Sample Format -->
            <div class="p-6 rounded border" style="background-color: var(--bg-secondary); border-color: var(--border-color);">
              <h3 class="text-lg font-semibold mb-4" style="color: var(--text-primary);">
                JSON Format Reference
              </h3>
              <p class="text-sm mb-2" style="color: var(--text-secondary);">
                Your import file should follow this structure:
              </p>
              <pre class="text-xs p-4 rounded overflow-x-auto" style="background-color: var(--bg-primary); color: var(--text-primary);">{{
`{
  "groups": [
    {
      "id": "group-1",
      "name": "My Servers",
      "color": "#9B59B6",
      "deviceCount": 2
    }
  ],
  "devices": [
    {
      "id": "device-1",
      "name": "Custom Server",
      "category": "My Servers",
      "ruSize": 2,
      "powerDraw": 850,
      "color": "#9B59B6",
      "description": "Custom device",
      "custom": true
    }
  ]
}`
              }}</pre>
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
    @click.self="closeGroupDialog"
  >
    <div class="rounded-xl shadow-2xl w-full max-w-md transform transition-all duration-200" style="background-color: var(--bg-primary);">
      <div class="flex items-center justify-between mb-6 p-6 rounded-t-xl" style="background-color: var(--color-primary);">
        <h2 class="text-2xl font-bold" style="color: #0c0c0d;">{{ editingGroup ? 'Edit' : 'Add' }} Device Group</h2>
        <button
          @click="closeGroupDialog"
          class="transition-colors"
          style="color: rgba(12, 12, 13, 0.7);"
          @mouseover="$event.currentTarget.style.color = '#0c0c0d'"
          @mouseout="$event.currentTarget.style.color = 'rgba(12, 12, 13, 0.7)'"
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
            @click="closeGroupDialog"
            class="flex-1 px-4 py-2 rounded transition-colors"
            style="background-color: var(--bg-secondary); color: var(--text-primary);"
            @mouseover="$event.currentTarget.style.backgroundColor = 'var(--border-color)'"
            @mouseout="$event.currentTarget.style.backgroundColor = 'var(--bg-secondary)'"
          >
            Cancel
          </button>
          <button
            @click="handleSaveGroup"
            :disabled="!newGroup.name?.trim()"
            class="flex-1 px-4 py-2 text-white rounded transition-colors"
            :style="{
              backgroundColor: !newGroup.name?.trim() ? 'var(--color-primary-light)' : 'var(--color-primary)',
              opacity: !newGroup.name?.trim() ? '0.5' : '1',
              cursor: !newGroup.name?.trim() ? 'not-allowed' : 'pointer'
            }"
          >
            {{ editingGroup ? 'Save Changes' : 'Add Group' }}
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
    @click.self="closeDeviceDialog"
  >
    <div class="rounded-xl shadow-2xl w-full max-w-md transform transition-all duration-200" style="background-color: var(--bg-primary);">
      <div class="flex items-center justify-between mb-6 p-6 rounded-t-xl" style="background-color: var(--color-primary);">
        <h2 class="text-2xl font-bold" style="color: #0c0c0d;">
          {{ editingDevice ? 'Edit' : isDuplicating ? 'Duplicate' : 'Add' }} Device
        </h2>
        <button
          @click="closeDeviceDialog"
          class="transition-colors"
          style="color: rgba(12, 12, 13, 0.7);"
          @mouseover="$event.currentTarget.style.color = '#0c0c0d'"
          @mouseout="$event.currentTarget.style.color = 'rgba(12, 12, 13, 0.7)'"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="px-6 pb-6" style="max-height: 70vh; overflow-y: auto;">
        <div class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            Device Model Name *
          </label>
          <input
            v-model="newDevice.name"
            type="text"
            placeholder="e.g., Dell PowerEdge R750"
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            :style="{
              border: `1px solid ${validationErrors.name ? '#ef4444' : 'var(--border-color)'}`,
              backgroundColor: 'var(--bg-secondary)',
              color: 'var(--text-primary)'
            }"
          />
          <p v-if="validationErrors.name" class="text-xs mt-1" style="color: #ef4444;">
            {{ validationErrors.name }}
          </p>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            Device Group *
          </label>
          <select
            v-model="newDevice.category"
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            :style="{
              border: `1px solid ${validationErrors.category ? '#ef4444' : 'var(--border-color)'}`,
              backgroundColor: 'var(--bg-secondary)',
              color: 'var(--text-primary)'
            }"
          >
            <option value="">Select a group...</option>
            <option v-for="group in deviceGroups" :key="group.id" :value="group.name">
              {{ group.name }}
            </option>
          </select>
          <p v-if="validationErrors.category" class="text-xs mt-1" style="color: #ef4444;">
            {{ validationErrors.category }}
          </p>
          <p v-else class="text-xs mt-1" style="color: var(--text-secondary);">
            Create new groups in the "Device Groups" tab
          </p>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            RU Size (Rack Units) *
          </label>
          <input
            v-model.number="newDevice.ruSize"
            type="number"
            min="1"
            max="42"
            placeholder="e.g., 2"
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            :style="{
              border: `1px solid ${validationErrors.ruSize ? '#ef4444' : 'var(--border-color)'}`,
              backgroundColor: 'var(--bg-secondary)',
              color: 'var(--text-primary)'
            }"
          />
          <p v-if="validationErrors.ruSize" class="text-xs mt-1" style="color: #ef4444;">
            {{ validationErrors.ruSize }}
          </p>
          <p v-else class="text-xs mt-1" style="color: var(--text-secondary);">
            1U = 1.75 inches (44.45mm)
          </p>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            Power Draw (Watts) *
          </label>
          <input
            v-model.number="newDevice.powerDraw"
            type="number"
            min="0"
            placeholder="e.g., 750"
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            :style="{
              border: `1px solid ${validationErrors.powerDraw ? '#ef4444' : 'var(--border-color)'}`,
              backgroundColor: 'var(--bg-secondary)',
              color: 'var(--text-primary)'
            }"
          />
          <p v-if="validationErrors.powerDraw" class="text-xs mt-1" style="color: #ef4444;">
            {{ validationErrors.powerDraw }}
          </p>
          <p v-else class="text-xs mt-1" style="color: var(--text-secondary);">
            Maximum power consumption under load
          </p>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            Power Ports Used *
          </label>
          <input
            v-model.number="newDevice.powerPortsUsed"
            type="number"
            min="0"
            placeholder="e.g., 2 for dual PSU"
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            :style="{
              border: `1px solid ${validationErrors.powerPortsUsed ? '#ef4444' : 'var(--border-color)'}`,
              backgroundColor: 'var(--bg-secondary)',
              color: 'var(--text-primary)'
            }"
          />
          <p v-if="validationErrors.powerPortsUsed" class="text-xs mt-1" style="color: #ef4444;">
            {{ validationErrors.powerPortsUsed }}
          </p>
          <p v-else class="text-xs mt-1" style="color: var(--text-secondary);">
            Number of PDU power ports required (1 for single PSU, 2 for dual PSU, etc.)
          </p>
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
            @click="closeDeviceDialog"
            class="flex-1 px-4 py-2 rounded transition-colors"
            style="background-color: var(--bg-secondary); color: var(--text-primary);"
            @mouseover="$event.currentTarget.style.backgroundColor = 'var(--border-color)'"
            @mouseout="$event.currentTarget.style.backgroundColor = 'var(--bg-secondary)'"
          >
            Cancel
          </button>
          <button
            @click="handleSaveDevice"
            :disabled="!canAddDevice"
            class="flex-1 px-4 py-2 text-white rounded transition-colors"
            :style="{
              backgroundColor: !canAddDevice ? 'var(--color-primary-light)' : 'var(--color-primary)',
              opacity: !canAddDevice ? '0.5' : '1',
              cursor: !canAddDevice ? 'not-allowed' : 'pointer'
            }"
          >
            {{ editingDevice ? 'Save Changes' : isDuplicating ? 'Create Duplicate' : 'Add Device' }}
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Add/Edit Resource Provider Dialog -->
  <div
    v-if="showAddProviderDialog"
    class="fixed inset-0 flex items-center justify-center z-50 transition-opacity duration-200"
    style="background-color: rgba(0, 0, 0, 0.3); backdrop-filter: blur(4px);"
    @click.self="closeProviderDialog"
  >
    <div class="rounded-xl shadow-2xl w-full max-w-md transform transition-all duration-200" style="background-color: var(--bg-primary);">
      <div class="flex items-center justify-between mb-6 p-6 rounded-t-xl" style="background-color: var(--color-primary);">
        <h2 class="text-2xl font-bold" style="color: #0c0c0d;">
          {{ editingProvider ? 'Edit' : 'Add' }} Resource Provider
        </h2>
        <button
          @click="closeProviderDialog"
          class="transition-colors"
          style="color: rgba(12, 12, 13, 0.7);"
          @mouseover="$event.currentTarget.style.color = '#0c0c0d'"
          @mouseout="$event.currentTarget.style.color = 'rgba(12, 12, 13, 0.7)'"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="px-6 pb-6" style="max-height: 70vh; overflow-y: auto;">
        <div class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            Provider Name *
          </label>
          <input
            v-model="newProvider.name"
            type="text"
            placeholder="e.g., PDU-A01, CRAC-02, Network Switch"
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
          />
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            Provider Type *
          </label>
          <select
            v-model="newProvider.type"
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
          >
            <option value="">Select type...</option>
            <option value="power">Power (PDU, UPS, Generator)</option>
            <option value="cooling">Cooling (HVAC, CRAC, CRAH)</option>
            <option value="network">Network (Switch, Router, Uplink)</option>
          </select>
          <p class="text-xs mt-1" style="color: var(--text-secondary);">
            What type of resource does this provide?
          </p>
        </div>

        <!-- Power Capacity (shown for power type) -->
        <div v-if="newProvider.type === 'power'" class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            Power Capacity (Watts) *
          </label>
          <input
            v-model.number="newProvider.powerCapacity"
            type="number"
            min="0"
            placeholder="e.g., 20000"
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
          />
          <p class="text-xs mt-1" style="color: var(--text-secondary);">
            Maximum power this provider can supply
          </p>
        </div>

        <!-- Power Ports Capacity (shown for power type) -->
        <div v-if="newProvider.type === 'power'" class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            Power Ports Capacity *
          </label>
          <input
            v-model.number="newProvider.powerPortsCapacity"
            type="number"
            min="0"
            placeholder="e.g., 24"
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
          />
          <p class="text-xs mt-1" style="color: var(--text-secondary);">
            Number of available power ports on this PDU
          </p>
        </div>

        <!-- Cooling Capacity (shown for cooling type) -->
        <div v-if="newProvider.type === 'cooling'" class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            Cooling Capacity (Refrigeration Tons) *
          </label>
          <input
            v-model.number="newProvider.coolingCapacityTons"
            type="number"
            min="0"
            step="0.1"
            placeholder="e.g., 5"
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
          />
          <p class="text-xs mt-1" style="color: var(--text-secondary);">
            1 Refrigeration Ton = 12,000 BTU/hr
          </p>
        </div>

        <!-- Network Capacity (shown for network type) -->
        <div v-if="newProvider.type === 'network'" class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            Network Capacity (Gbps) *
          </label>
          <input
            v-model.number="newProvider.networkCapacity"
            type="number"
            min="0"
            step="0.1"
            placeholder="e.g., 10"
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
          />
          <p class="text-xs mt-1" style="color: var(--text-secondary);">
            Total bandwidth provided
          </p>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            Location (Optional)
          </label>
          <input
            v-model="newProvider.location"
            type="text"
            placeholder="e.g., Row A, Room 101, Cabinet 5"
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
          />
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            Description (Optional)
          </label>
          <textarea
            v-model="newProvider.description"
            rows="3"
            placeholder="Additional details about this provider..."
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
          ></textarea>
        </div>

        <div class="flex gap-2">
          <button
            @click="closeProviderDialog"
            class="flex-1 px-4 py-2 rounded transition-colors"
            style="background-color: var(--bg-secondary); color: var(--text-primary);"
            @mouseover="$event.currentTarget.style.backgroundColor = 'var(--border-color)'"
            @mouseout="$event.currentTarget.style.backgroundColor = 'var(--bg-secondary)'"
          >
            Cancel
          </button>
          <button
            @click="handleSaveProvider"
            :disabled="!canAddProvider"
            class="flex-1 px-4 py-2 text-white rounded transition-colors"
            :style="{
              backgroundColor: !canAddProvider ? 'var(--color-primary-light)' : 'var(--color-primary)',
              opacity: !canAddProvider ? '0.5' : '1',
              cursor: !canAddProvider ? 'not-allowed' : 'pointer'
            }"
          >
            {{ editingProvider ? 'Save Changes' : 'Add Provider' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useToast } from '../composables/useToast';
import { useResourceProviders } from '../composables/useResourceProviders';

const { showToast } = useToast();
const { 
  resourceProviders,
  addProvider: addResourceProvider,
  updateProvider: updateResourceProvider,
  deleteProvider: deleteResourceProvider
} = useResourceProviders();

const activeTab = ref('groups');
const showAddGroupDialog = ref(false);
const showAddDeviceDialog = ref(false);
const showAddProviderDialog = ref(false);
const editingGroup = ref(null);
const editingDevice = ref(null);
const editingProvider = ref(null);
const isDuplicating = ref(false);

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
  powerPortsUsed: 1,
  color: '',
  description: ''
});

const validationErrors = ref({
  name: '',
  category: '',
  ruSize: '',
  powerDraw: ''
});

const newProvider = ref({
  name: '',
  type: '',
  powerCapacity: 0,
  powerPortsCapacity: 0,
  coolingCapacityTons: 0,
  networkCapacity: 0,
  location: '',
  description: ''
});

const importMode = ref('merge');
const importError = ref('');
const fileInput = ref(null);

const canAddDevice = computed(() => {
  return newDevice.value.name?.trim() &&
         newDevice.value.category &&
         newDevice.value.ruSize > 0 &&
         newDevice.value.powerDraw >= 0 &&
         newDevice.value.powerPortsUsed >= 0;
});

const canAddProvider = computed(() => {
  if (!newProvider.value.name?.trim() || !newProvider.value.type) {
    return false;
  }
  
  // Check that at least one capacity is provided for the selected type
  if (newProvider.value.type === 'power') {
    return newProvider.value.powerCapacity > 0;
  } else if (newProvider.value.type === 'cooling') {
    return newProvider.value.coolingCapacityTons > 0;
  } else if (newProvider.value.type === 'network') {
    return newProvider.value.networkCapacity > 0;
  }
  
  return false;
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

function validateDevice() {
  validationErrors.value = {
    name: '',
    category: '',
    ruSize: '',
    powerDraw: ''
  };

  let isValid = true;

  if (!newDevice.value.name?.trim()) {
    validationErrors.value.name = 'Device name is required';
    isValid = false;
  } else if (newDevice.value.name.length < 3) {
    validationErrors.value.name = 'Device name must be at least 3 characters';
    isValid = false;
  }

  if (!newDevice.value.category) {
    validationErrors.value.category = 'Please select a device group';
    isValid = false;
  }

  if (!newDevice.value.ruSize || newDevice.value.ruSize < 1 || newDevice.value.ruSize > 42) {
    validationErrors.value.ruSize = 'RU size must be between 1 and 42';
    isValid = false;
  }

  if (newDevice.value.powerDraw === null || newDevice.value.powerDraw === undefined || newDevice.value.powerDraw < 0) {
    validationErrors.value.powerDraw = 'Power draw must be 0 or greater';
    isValid = false;
  }

  return isValid;
}

function closeGroupDialog() {
  showAddGroupDialog.value = false;
  editingGroup.value = null;
  newGroup.value = {
    name: '',
    color: '#4A90E2'
  };
}

function closeDeviceDialog() {
  showAddDeviceDialog.value = false;
  editingDevice.value = null;
  isDuplicating.value = false;
  newDevice.value = {
    name: '',
    category: '',
    ruSize: 1,
    powerDraw: 0,
    powerPortsUsed: 1,
    color: '',
    description: ''
  };
  validationErrors.value = {
    name: '',
    category: '',
    ruSize: '',
    powerDraw: ''
  };
}

function editGroup(group) {
  editingGroup.value = group;
  newGroup.value = {
    name: group.name,
    color: group.color
  };
  showAddGroupDialog.value = true;
}

function handleSaveGroup() {
  if (!newGroup.value.name?.trim()) return;

  if (editingGroup.value) {
    // Update existing group
    const index = deviceGroups.value.findIndex(g => g.id === editingGroup.value.id);
    if (index !== -1) {
      deviceGroups.value[index] = {
        ...deviceGroups.value[index],
        name: newGroup.value.name.trim(),
        color: newGroup.value.color
      };
      
      // Update category name in devices if group name changed
      if (editingGroup.value.name !== newGroup.value.name.trim()) {
        customDevices.value.forEach(device => {
          if (device.category === editingGroup.value.name) {
            device.category = newGroup.value.name.trim();
          }
        });
        saveCustomDevices();
      }
      
      showToast('success', 'Device group updated');
    }
  } else {
    // Add new group
    const group = {
      id: `group-${Date.now()}`,
      name: newGroup.value.name.trim(),
      color: newGroup.value.color,
      deviceCount: 0
    };
    deviceGroups.value.push(group);
    showToast('success', 'Device group added');
  }

  saveDeviceGroups();
  closeGroupDialog();
  
  // Notify other components
  window.dispatchEvent(new CustomEvent('devices-updated'));
}

function deleteGroup(groupId) {
  const group = deviceGroups.value.find(g => g.id === groupId);
  if (!confirm(`Delete device group "${group.name}"? Devices in this group will not be deleted.`)) {
    return;
  }

  deviceGroups.value = deviceGroups.value.filter(g => g.id !== groupId);
  saveDeviceGroups();
  showToast('success', 'Device group deleted');
  
  // Notify other components
  window.dispatchEvent(new CustomEvent('devices-updated'));
}

function editDevice(device) {
  editingDevice.value = device;
  isDuplicating.value = false;
  newDevice.value = {
    name: device.name,
    category: device.category,
    ruSize: device.ruSize,
    powerDraw: device.powerDraw,
    powerPortsUsed: device.powerPortsUsed || 1,
    color: device.color,
    description: device.description || ''
  };
  showAddDeviceDialog.value = true;
}

function duplicateDevice(device) {
  editingDevice.value = null;
  isDuplicating.value = true;
  newDevice.value = {
    name: `${device.name} (Copy)`,
    category: device.category,
    ruSize: device.ruSize,
    powerDraw: device.powerDraw,
    powerPortsUsed: device.powerPortsUsed || 1,
    color: device.color,
    description: device.description || ''
  };
  showAddDeviceDialog.value = true;
}

function handleSaveDevice() {
  if (!validateDevice()) return;

  // Get color from group if not specified
  let color = newDevice.value.color;
  if (!color) {
    const group = deviceGroups.value.find(g => g.name === newDevice.value.category);
    color = group?.color || '#4A90E2';
  }

  if (editingDevice.value && !isDuplicating.value) {
    // Update existing device
    const index = customDevices.value.findIndex(d => d.id === editingDevice.value.id);
    if (index !== -1) {
      customDevices.value[index] = {
        ...customDevices.value[index],
        name: newDevice.value.name.trim(),
        category: newDevice.value.category,
        ruSize: newDevice.value.ruSize,
        powerDraw: newDevice.value.powerDraw,
        color: color,
        description: newDevice.value.description?.trim() || ''
      };
      showToast('success', 'Device updated');
    }
  } else {
    // Add new device (or duplicate)
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
    showToast('success', isDuplicating.value ? 'Device duplicated' : 'Device added');
  }

  saveCustomDevices();
  updateGroupCounts();
  closeDeviceDialog();
  
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

function closeProviderDialog() {
  showAddProviderDialog.value = false;
  editingProvider.value = null;
  newProvider.value = {
    name: '',
    type: '',
    powerCapacity: 0,
    powerPortsCapacity: 0,
    coolingCapacityTons: 0,
    networkCapacity: 0,
    location: '',
    description: ''
  };
}

function editProvider(provider) {
  editingProvider.value = provider;
  newProvider.value = {
    name: provider.name,
    type: provider.type,
    powerCapacity: provider.powerCapacity || 0,
    powerPortsCapacity: provider.powerPortsCapacity || 0,
    coolingCapacityTons: provider.coolingCapacity ? provider.coolingCapacity / 12000 : 0,
    networkCapacity: provider.networkCapacity || 0,
    location: provider.location || '',
    description: provider.description || ''
  };
  showAddProviderDialog.value = true;
}

function handleSaveProvider() {
  if (!canAddProvider.value) return;

  const providerData = {
    name: newProvider.value.name.trim(),
    type: newProvider.value.type,
    powerCapacity: newProvider.value.type === 'power' ? newProvider.value.powerCapacity : 0,
    coolingCapacity: newProvider.value.type === 'cooling' ? newProvider.value.coolingCapacityTons * 12000 : 0,
    networkCapacity: newProvider.value.type === 'network' ? newProvider.value.networkCapacity : 0,
    location: newProvider.value.location?.trim() || '',
    description: newProvider.value.description?.trim() || ''
  };

  if (editingProvider.value) {
    // Update existing provider
    updateResourceProvider(editingProvider.value.id, providerData);
    showToast('success', 'Resource provider updated');
  } else {
    // Add new provider
    addResourceProvider(providerData);
    showToast('success', 'Resource provider added');
  }

  closeProviderDialog();
}

function deleteProvider(providerId) {
  const provider = resourceProviders.value.find(p => p.id === providerId);
  if (!confirm(`Delete resource provider "${provider.name}"?`)) {
    return;
  }

  deleteResourceProvider(providerId);
  showToast('success', 'Resource provider deleted');
}

function exportDevices() {
  const exportData = {
    groups: deviceGroups.value,
    devices: customDevices.value,
    exportDate: new Date().toISOString(),
    version: '1.0'
  };

  const dataStr = JSON.stringify(exportData, null, 2);
  const dataBlob = new Blob([dataStr], { type: 'application/json' });
  const url = URL.createObjectURL(dataBlob);
  
  const link = document.createElement('a');
  link.href = url;
  link.download = `racksum-devices-${new Date().toISOString().split('T')[0]}.json`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
  
  showToast('success', 'Devices exported successfully');
}

function handleFileSelect(event) {
  const file = event.target.files[0];
  if (!file) return;
  
  importError.value = '';
  
  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const data = JSON.parse(e.target.result);
      importDevices(data);
    } catch (err) {
      importError.value = 'Invalid JSON file. Please check the file format.';
      console.error('Import error:', err);
    }
  };
  
  reader.onerror = () => {
    importError.value = 'Error reading file. Please try again.';
  };
  
  reader.readAsText(file);
  
  // Reset file input
  event.target.value = '';
}

function importDevices(data) {
  try {
    // Validate data structure
    if (!data.groups || !Array.isArray(data.groups)) {
      throw new Error('Invalid data: missing or invalid "groups" array');
    }
    if (!data.devices || !Array.isArray(data.devices)) {
      throw new Error('Invalid data: missing or invalid "devices" array');
    }
    
    // Validate required fields
    for (const group of data.groups) {
      if (!group.name || !group.color) {
        throw new Error('Invalid group: missing required fields (name, color)');
      }
    }
    
    for (const device of data.devices) {
      if (!device.name || !device.category || device.ruSize === undefined || device.powerDraw === undefined) {
        throw new Error('Invalid device: missing required fields (name, category, ruSize, powerDraw)');
      }
    }
    
    if (importMode.value === 'replace') {
      // Replace mode: clear existing data
      if (!confirm('This will replace all your existing custom devices and groups. Continue?')) {
        return;
      }
      deviceGroups.value = data.groups;
      customDevices.value = data.devices;
    } else {
      // Merge mode: combine with existing data
      const existingGroupIds = new Set(deviceGroups.value.map(g => g.id));
      const existingDeviceIds = new Set(customDevices.value.map(d => d.id));
      
      let groupsAdded = 0;
      let devicesAdded = 0;
      
      // Add new groups
      for (const group of data.groups) {
        if (!existingGroupIds.has(group.id)) {
          deviceGroups.value.push(group);
          groupsAdded++;
        }
      }
      
      // Add new devices
      for (const device of data.devices) {
        if (!existingDeviceIds.has(device.id)) {
          customDevices.value.push(device);
          devicesAdded++;
        }
      }
      
      showToast('success', `Imported ${groupsAdded} groups and ${devicesAdded} devices`);
    }
    
    saveDeviceGroups();
    saveCustomDevices();
    updateGroupCounts();
    
    if (importMode.value === 'replace') {
      showToast('success', 'Devices replaced successfully');
    }
    
    // Notify other components
    window.dispatchEvent(new CustomEvent('devices-updated'));
  } catch (err) {
    importError.value = err.message;
    console.error('Import error:', err);
  }
}
</script>
