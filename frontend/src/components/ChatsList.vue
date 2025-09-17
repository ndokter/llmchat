<script setup lang="ts">
import { inject, onMounted } from 'vue'
</script>

<template>
    <div class="chats-list">
        <ul>
            <li>A new chat</li>
            <li>A new chat2</li>
            <li>A new chat3</li>
        </ul>
    </div>
</template>

<style scoped>
ul {
    list-style: none;
    padding-left: 0;
    margin-left: 0;
}
</style>