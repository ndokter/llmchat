<script setup lang="ts">
import { inject, onMounted, onUnmounted } from 'vue'
import { useEventStore } from '@/stores/eventStore'
import ChatsList from './ChatsList.vue'

const eventStore = useEventStore()

// Initialize event connection when component is mounted
onMounted(() => {
  // Connect to event stream if not already connected
  if (!eventStore.isConnected && !eventStore.isConnecting) {
    eventStore.connect()
  }

  // Subscribe to events
  // This will be reactive to store changes
})

// Clean up when component is unmounted
onUnmounted(() => {
  // Connection will be maintained for other components
  // but we could implement logic to disconnect if needed
})
</script>

<template>
    <div class="sidebar">
        <ChatsList />
    </div>
</template>

<style scoped>
.sidebar {
    width: 220px;
    background: #140079ff;
    color: #fff;
    padding: 1rem;
}
</style>