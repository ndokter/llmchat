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
}

.sidebar-wrapper {
  width: 200px;
  flex: 0 0 200px;
  background: #140079ff;
}

.chat-wrapper {
  flex: 1;
  overflow: hidden;
}
</style>
