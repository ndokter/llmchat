<script setup lang="ts">
import ChatsList from './ChatsList.vue'
import router from '@/router'

const makeNewChat = () => {
    router.push({name: 'home'})
}
</script>

<template>
    <div class="sidebar">
        <div class="sidebar-section">
            <div @click="makeNewChat" class="sidebar-item">New chat</div>
        </div>

        <div class="sidebar-section">
            <div class="sidebar-title">Chats</div>
            <ChatsList />
        </div>
    </div>
</template>

<style scoped>

</style>