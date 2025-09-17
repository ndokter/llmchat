<script setup lang="ts">
import { inject, onMounted } from 'vue'
import ChatsList from './ChatsList.vue'
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