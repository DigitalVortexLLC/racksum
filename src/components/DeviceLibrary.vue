<template>
  <aside class="shadow-lg overflow-y-auto border-r bg-base-100 border-base-300">
    <div
      class="px-6 flex items-center bg-secondary"
      style="min-height: 68px;"
    >
      <h2 class="text-2xl font-bold text-secondary-content">
        Library
      </h2>
    </div>

    <!-- Tabs -->
    <div
      role="tablist"
      class="tabs tabs-border"
    >
      <button
        role="tab"
        class="tab flex-1"
        :class="{ 'tab-active': activeTab === 'devices' }"
        @click="activeTab = 'devices'"
      >
        Devices
      </button>
      <button
        role="tab"
        class="tab flex-1"
        :class="{ 'tab-active': activeTab === 'providers' }"
        @click="activeTab = 'providers'"
      >
        Providers
      </button>
    </div>

    <!-- Devices Tab Content -->
    <div
      v-show="activeTab === 'devices'"
      class="p-4"
    >
      <!-- Manage Button -->
      <button
        class="btn btn-primary btn-sm btn-block gap-2 mb-4"
        @click="$emit('open-device-manager', 'devices')"
      >
        <svg
          class="size-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 6v6m0 0v6m0-6h6m-6 0H6"
          />
        </svg>
        Manage Devices & Groups
      </button>

      <!-- Search bar -->
      <input
        v-model="deviceSearchQuery"
        type="text"
        placeholder="Search devices..."
        class="input input-sm w-full mb-4"
      >

      <!-- Device Categories -->
      <div
        v-for="category in filteredCategories"
        :key="category.id"
        class="mb-2"
      >
        <DeviceCategory
          :category="category"
          :search-query="deviceSearchQuery"
        />
      </div>

      <div
        v-if="filteredCategories.length === 0"
        class="text-center py-8 opacity-70"
      >
        No devices found
      </div>
    </div>

    <!-- Resource Providers Tab Content -->
    <div
      v-show="activeTab === 'providers'"
      class="p-4"
    >
      <!-- Manage Button -->
      <button
        class="btn btn-primary btn-sm btn-block gap-2 mb-4"
        @click="$emit('open-device-manager', 'providers')"
      >
        <svg
          class="size-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 6v6m0 0v6m0-6h6m-6 0H6"
          />
        </svg>
        Manage Providers
      </button>

      <!-- Search bar -->
      <input
        v-model="providerSearchQuery"
        type="text"
        placeholder="Search providers..."
        class="input input-sm w-full mb-4"
      >

      <!-- No providers message -->
      <div
        v-if="templateProviders.length === 0"
        class="text-center py-8"
      >
        <p class="text-sm mb-2 opacity-70">
          No resource providers configured
        </p>
        <p class="text-xs opacity-70">
          Click "Manage Providers" above to add
        </p>
      </div>

      <!-- Provider Groups by Type -->
      <div
        v-for="providerGroup in filteredProviderGroups"
        :key="providerGroup.type"
        class="mb-4"
      >
        <h3 class="text-sm font-semibold mb-2 px-2">
          {{ providerGroup.name }}
        </h3>
        
        <div
          v-for="provider in providerGroup.providers"
          :key="provider.id"
          class="card bg-base-200 p-3 mb-2 cursor-grab active:cursor-grabbing hover:border-primary"
          draggable="true"
          @dragstart="handleDragStart($event, provider)"
          @dragend="handleDragEnd"
        >
          <div class="flex items-start gap-3">
            <!-- Icon -->
            <div class="flex-shrink-0 mt-0.5">
              <svg
                v-if="provider.type === 'power'"
                class="w-5 h-5 text-primary"
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
                class="w-5 h-5 text-primary"
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
                class="w-5 h-5 text-primary"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
              </svg>
            </div>

            <!-- Info -->
            <div class="flex-1 min-w-0">
              <div class="font-medium text-sm truncate">
                {{ provider.name }}
              </div>
              <div class="text-xs opacity-70">
                <span v-if="provider.powerCapacity > 0">{{ provider.powerCapacity.toLocaleString() }}W</span>
                <span v-if="provider.coolingCapacity > 0">{{ (provider.coolingCapacity / 12000).toFixed(1) }} Tons</span>
                <span v-if="provider.networkCapacity > 0">{{ provider.networkCapacity }} Gbps</span>
              </div>
              <div
                v-if="provider.location"
                class="text-xs mt-1 truncate opacity-70"
              >
                📍 {{ provider.location }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Info about provider templates -->
      <div
        v-if="templateProviders.length > 0"
        class="mt-6 pt-4 border-t border-base-300"
      >
        <div class="alert alert-info">
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
          <span class="text-xs">Drag providers to racks or unracked devices to add capacity.</span>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useDevices } from '../composables/useDevices'
import { useResourceProviders } from '../composables/useResourceProviders'
import { useDragDrop } from '../composables/useDragDrop'
import DeviceCategory from './DeviceCategory.vue'

defineEmits(['open-device-manager'])

const activeTab = ref('devices')
const deviceSearchQuery = ref('')
const providerSearchQuery = ref('')

// Devices
const { categories } = useDevices()

// Drag and drop
const { startDrag } = useDragDrop()

const filteredCategories = computed(() => {
  if (!deviceSearchQuery.value) return categories.value

  return categories.value
    .map(category => ({
      ...category,
      devices: category.devices.filter(device =>
        device.name.toLowerCase().includes(deviceSearchQuery.value.toLowerCase()) ||
        device.description.toLowerCase().includes(deviceSearchQuery.value.toLowerCase())
      )
    }))
    .filter(category => category.devices.length > 0)
})

// Resource Providers
const {
  getTemplateProviders
} = useResourceProviders()

const templateProviders = getTemplateProviders

const filteredProviderGroups = computed(() => {
  const groups = [
    {
      type: 'power',
      name: 'Power Providers',
      providers: templateProviders.value.filter(p => p.type === 'power')
    },
    {
      type: 'cooling',
      name: 'Cooling Providers',
      providers: templateProviders.value.filter(p => p.type === 'cooling')
    },
    {
      type: 'network',
      name: 'Network Providers',
      providers: templateProviders.value.filter(p => p.type === 'network')
    }
  ].filter(group => group.providers.length > 0)

  if (!providerSearchQuery.value) return groups

  const query = providerSearchQuery.value.toLowerCase()
  return groups
    .map(group => ({
      ...group,
      providers: group.providers.filter(provider =>
        provider.name.toLowerCase().includes(query) ||
        (provider.location && provider.location.toLowerCase().includes(query)) ||
        (provider.description && provider.description.toLowerCase().includes(query))
      )
    }))
    .filter(group => group.providers.length > 0)
})

// Drag and drop handlers for providers
import { useDragDrop } from '../composables/useDragDrop'

const { startDrag } = useDragDrop()

const handleDragStart = (event, provider) => {
  startDrag(event, provider, { type: 'provider-library' })
  event.target.style.opacity = '0.5'
}

const handleDragEnd = (event) => {
  event.target.style.opacity = '1'
}
</script>