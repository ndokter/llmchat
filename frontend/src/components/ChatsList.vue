<script setup lang="ts">
import { inject, onMounted, onUnmounted, ref } from 'vue'
import { useEventStore } from '@/stores/eventStore'
import ChatsList from './ChatsList.vue'

const eventStore = useEventStore()
const chatHistory = ref([])

onMounted(async () => {
  await getChatHistory()
  console.log(chatHistory.value)
})

onUnmounted(() => {

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
      <li v-for="chat in chatHistory">
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
  padding: 3px 10px;
  border-radius: 3px;
}
li:hover {
  background: #2200cb
  
}
a {
  text-decoration: none;
  color: #fff
}
</style>