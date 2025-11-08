<template>
  <aside class="shadow-lg overflow-y-auto transition-colors border-r" style="background-color: var(--bg-primary); border-color: var(--border-color);">
    <div class="px-6 flex items-center" style="background-color: var(--color-primary-dark); min-height: 68px;">
      <h2 class="text-2xl font-bold leading-none" style="color: #0c0c0d;">Device Library</h2>
    </div>

    <div class="p-4">
      <!-- Search bar -->
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search devices..."
        class="w-full px-3 py-2 rounded mb-4 focus:outline-none transition-colors"
        style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
        @focus="$event.target.style.borderColor = 'var(--color-primary)'"
        @blur="$event.target.style.borderColor = 'var(--border-color)'"
      />

      <!-- Device Categories -->
      <div v-for="category in filteredCategories" :key="category.id" class="mb-2">
        <DeviceCategory :category="category" :search-query="searchQuery" />
      </div>

      <div v-if="filteredCategories.length === 0" class="text-center py-8" style="color: var(--text-secondary);">
        No devices found
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useDevices } from '../composables/useDevices'
import DeviceCategory from './DeviceCategory.vue'

const searchQuery = ref('')
const { categories } = useDevices()

const filteredCategories = computed(() => {
  if (!searchQuery.value) return categories.value

  return categories.value
    .map(category => ({
      ...category,
      devices: category.devices.filter(device =>
        device.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        device.description.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    }))
    .filter(category => category.devices.length > 0)
})
</script>