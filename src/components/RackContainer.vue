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

      <!-- Add Rack Button -->
      <button
        @click="handleAddRack"
        class="rounded-lg shadow-lg p-4 flex-shrink-0 transition-all duration-200 flex items-center justify-center"
        style="width: 250px; background-color: var(--bg-primary); border: 2px dashed var(--border-color);"
        @mouseover="$event.target.style.borderColor = 'var(--color-primary)'; $event.target.style.backgroundColor = 'var(--bg-secondary)'"
        @mouseout="$event.target.style.borderColor = 'var(--border-color)'; $event.target.style.backgroundColor = 'var(--bg-primary)'"
        title="Add new rack"
      >
        <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="color: var(--color-primary);">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
      </button>
    </div>

    <div v-if="racks.length === 0" class="text-center py-20" style="color: var(--text-secondary);">
      <p class="text-xl mb-2">No racks configured</p>
      <p class="text-sm">Click the + button to add your first rack</p>
    </div>
  </div>
</template>

<script setup>
import { useRackConfig } from '../composables/useRackConfig'
import { useToast } from '../composables/useToast'
import { useDatabase } from '../composables/useDatabase'
import Rack from './Rack.vue'

const { racks, addRack } = useRackConfig()
const { showSuccess } = useToast()
const { currentSite } = useDatabase()

const handleAddRack = () => {
  const newRack = addRack()
  showSuccess('Rack Added', `${newRack.name} has been created`)
}
</script>
