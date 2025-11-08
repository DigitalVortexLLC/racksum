<template>
  <div class="rack-container">
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
import Rack from './Rack.vue'

const { racks } = useRackConfig()
</script>