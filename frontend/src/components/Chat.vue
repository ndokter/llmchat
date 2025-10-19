<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useEventStore, type EventData, type EventHandler } from '@/stores/eventStore'
import router from '@/router'
import ChatMessage from '../components/ChatMessage.vue'
import ChatInput from '../components/ChatInput.vue'

const route = useRoute()
const eventStore = useEventStore()

interface Chat {
  messages?: Array<{
    id: number
    message: string
    role: string
    parent_id: number | null
  }>
}

const chat = ref<Chat>({})

const eventStreamHandler = (e: EventData) => {   
    if (e.type === "chat:completion") {
        const {chat_id, message_id, content, status } = e.body

        if (chat.value.messages) {
            const messageIndex = chat.value.messages.findIndex(m => m.id === message_id)
            if (messageIndex > -1) {
                chat.value.messages[messageIndex].message = content
            }
        }
    }
}

const sendMessage = (formData: { query: string, model: string }) => {
    fetch(`${import.meta.env.VITE_API_URL}/chat-message`, {
        method: "POST",
        body: JSON.stringify({
            "chat_id": route.params.id ?? null,
            "model_id": 1,
            "parent_id": null,
            "message": formData.query
        }),
        headers: {"Content-Type": "application/json"}
    })
    .then((response) => response.json())
    .then((data) => {
        if (!route.params.id) {
            router.push({name: 'chat', params: { id: data.id}})
        }

        chat.value = data
    })
}

const loadChat = async (id: any) => {
  const response = await fetch(`${import.meta.env.VITE_API_URL}/chats/${id}`, {
      method: "GET",
      headers: {"Content-Type": "application/json"}
  })
  if (response.ok) {
    chat.value = await response.json()
    // console.log(chat)
  }
}

watch(
  () => route.params.id,
  (chatId) => {
    if (chatId) {
      loadChat(chatId)
    } else {
      chat.value = {}
    }
  },
  { immediate: true }
)


onMounted(() => {
    eventStore.subscribe(eventStreamHandler)
})

onUnmounted(() => {
    eventStore.unsubscribe(eventStreamHandler)
})


</script>

<template>
    <div class="chat">
        <div id="chat-messages">
            <ChatMessage v-for="message in chat.messages" :message="message" />
        </div>

        <ChatInput @submit="sendMessage" />
    </div>
</template>

<style scoped>
.chat {
    flex: 1;
    background: #fff;
    height: 100%;
    display: flex;
    flex-direction: column;
    margin-left: 50px;
    margin-right: 50px;
}
#chat-messages {
    overflow-y: scroll;
    flex-grow: 1;
    padding: 10px 0 0 0;
    min-height: 0;
}
</style>