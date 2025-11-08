<template>
  <div class="rounded-lg shadow-lg p-4 flex-shrink-0 transition-colors" style="width: 250px; background-color: var(--bg-primary);">
    <!-- Rack Header -->
    <div class="mb-4 pb-2" style="border-bottom: 1px solid var(--border-color);">
      <input
        v-model="rack.name"
        class="text-lg font-semibold w-full focus:outline-none px-2 py-1 rounded transition-colors"
        style="background-color: transparent; color: var(--text-primary);"
        @blur="updateRackName"
        @focus="$event.target.style.backgroundColor = 'var(--bg-secondary)'"
      />
    </div>

    <!-- Rack Slots (numbered from top to bottom) -->
    <div class="space-y-0.5">
      <RackSlot
        v-for="position in totalRU"
        :key="position"
        :rack-id="rack.id"
        :position="position"
        :device="getDeviceAtPosition(position)"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRackConfig } from '../composables/useRackConfig'
import RackSlot from './RackSlot.vue'

const props = defineProps({
  rack: {
    type: Object,
    required: true
  }
})

const { config, updateRack } = useRackConfig()

const totalRU = computed(() => config.value.settings.ruPerRack || 42)

const getDeviceAtPosition = (position) => {
  return props.rack.devices.find(device => {
    const deviceEnd = device.position + device.ruSize - 1
    return position >= device.position && position <= deviceEnd
  })
}

const updateRackName = () => {
  updateRack(props.rack.id, { name: props.rack.name })
}
</script>