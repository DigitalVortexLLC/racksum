<template>
  <div class="rounded transition-colors" style="border: 1px solid var(--border-color);">
    <!-- Accordion Header -->
    <button
      @click="isOpen = !isOpen"
      class="w-full px-4 py-3 flex items-center justify-between transition-colors"
      style="background-color: var(--bg-secondary);"
      @mouseover="$event.target.style.backgroundColor = 'var(--border-color)'"
      @mouseout="$event.target.style.backgroundColor = 'var(--bg-secondary)'"
    >
      <span class="font-medium" style="color: var(--text-primary);">{{ category.name }}</span>
      <svg
        :class="{ 'transform rotate-180': isOpen }"
        class="w-5 h-5 transition-transform"
        style="color: var(--text-secondary);"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <!-- Accordion Content -->
    <div v-show="isOpen" style="border-top: 1px solid var(--border-color);">
      <DeviceItem
        v-for="device in category.devices"
        :key="device.id"
        :device="device"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import DeviceItem from './DeviceItem.vue'

const props = defineProps({
  category: {
    type: Object,
    required: true
  },
  searchQuery: {
    type: String,
    default: ''
  }
})

// Auto-open if there's a search query
const isOpen = ref(props.searchQuery ? true : false)
</script>