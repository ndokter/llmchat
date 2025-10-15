<script setup lang="ts">
import SideBar from '../components/SideBar.vue'
import Chat from '../components/Chat.vue'
</script>

<template>
  <div class="layout">
    <div class="sidebar-wrapper">
      <SideBar />
    </div>
    <div class="chat-wrapper">
      <Chat />
    </div>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.sidebar-wrapper {
  width: 260px;
  flex: 0 0 260px;
  height: 100vh;
  overflow-y: auto;
}

.chat-wrapper {
  flex: 1;
  overflow: hidden;
  height: 100vh;
}
</style>
