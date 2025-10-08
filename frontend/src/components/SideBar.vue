<script setup lang="ts">
import ChatsList from './ChatsList.vue'


</script>

<template>
    <div class="sidebar">
        <ChatsList />
    </div>
</template>

<style scoped>
.sidebar {
    flex: 1;
    background: #140079ff;
    max-height: 100vh;
    color: #fff;
    padding: 20px 10px;
    overflow-y: scroll;
}
</style>