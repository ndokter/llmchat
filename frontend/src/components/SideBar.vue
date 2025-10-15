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
            <div @click="makeNewChat" class="sidebar-item sidebar-action">
                <div class="icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                    <line x1="12" y1="6" x2="12" y2="14"/>
                    <line x1="8" y1="10" x2="16" y2="10"/>
                    </svg>
                </div>
                New Chat
            </div>
        </div>

        <div class="sidebar-section">
            <div class="sidebar-title">Chats</div>
            <ChatsList />
        </div>
    </div>
</template>

<style scoped>

</style>