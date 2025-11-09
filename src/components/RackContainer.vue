<template>
  <div class="rack-container">
    <!-- Site Name Title -->
    <div v-if="currentSite" class="mb-6">
      <h2 class="text-3xl font-bold" style="color: var(--text-primary);">
        {{ currentSite.name }}
      </h2>
      <p v-if="currentSite.description" class="text-sm mt-1" style="color: var(--text-secondary);">
        {{ currentSite.description }}
      </p>
    </div>

    <div class="flex gap-6 overflow-x-auto pb-4">
      <Rack
        v-for="rack in racks"
        :key="rack.id"
        :rack="rack"
      />
    </div>

    <div v-if="racks.length === 0" class="text-center text-gray-500 py-20">
      <p class="text-xl mb-2">No racks configured</p>
      <p class="text-sm">Click "Configure" to add racks</p>
    </div>
  </div>
</template>

<script setup>
import { useRackConfig } from '../composables/useRackConfig'
import { useDatabase } from '../composables/useDatabase'
import Rack from './Rack.vue'

const { racks } = useRackConfig()
const { currentSite } = useDatabase()
</script>