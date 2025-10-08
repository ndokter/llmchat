<script setup lang="ts">
import { inject, onMounted, onUnmounted, ref } from 'vue'
import { useEventStore, type EventData } from '@/stores/eventStore'
import { useRoute } from 'vue-router'

const route = useRoute()
const eventStore = useEventStore()
const chatHistory = ref([])


const eventStreamHandler = (e: EventData) => {   
    if (e.type === "chat:created" || e.type === "chat:title") {
        getChatHistory()
    }
}

onMounted(() => {
    eventStore.subscribe(eventStreamHandler)
    getChatHistory()
})

onUnmounted(() => {
    eventStore.unsubscribe(eventStreamHandler)
})


const getChatHistory = async () => {
  const response = await fetch(`${import.meta.env.VITE_API_URL}/chats`, {
    method: "GET",
    headers: {"Content-Type": "application/json"}
  })

  if (response.ok) {
    chatHistory.value = await response.json()
  }
}

</script>

<template>
  <div class="chats-list">
    <ul>
      <li v-for="chat in chatHistory" :class="{selected: route.params.id == chat.id }">
        <RouterLink :to="{name: 'chat', params: {id: chat.id}}">
          <div v-if="!chat.title">New chat</div>
          <div v-else>{{ chat.title }}</div>
        </RouterLink>
        <!-- {{ chat.updated_at }} -->
      </li>
    </ul>
  </div>
</template>

<style scoped>

ul {
  list-style: none;
  padding-left: 0;
  margin-left: 0;
}
li {
  margin-bottom: 3px;
  padding: 2px 10px;
  border-radius: 3px;
}
li:hover, li.selected {
  background: #2200cb
}
a {
  text-decoration: none;
  color: #fff
}
</style>