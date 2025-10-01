<script setup lang="ts">
import { inject, onMounted, onUnmounted } from 'vue'
import { useEventStore } from '@/stores/eventStore'
import ChatsList from './ChatsList.vue'

const eventStore = useEventStore()

onMounted(() => {
})

onUnmounted(() => {

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
    /* padding: 1rem; */
    padding: 20px 10px;
}
</style>