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
    flex: 1;
    /* width: 220px;
    position:relative; */
    background: #140079ff;
    color: #fff;
    padding: 20px 10px;
    overflow-y: scroll;
}
</style>