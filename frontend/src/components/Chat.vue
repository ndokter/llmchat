<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useEventStore, type EventData, type EventHandler } from '@/stores/eventStore'
import router from '@/router'
import ChatMessage from '../components/ChatMessage.vue'

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

const sendMessage = (submitEvent: Event) => {
    const form = submitEvent.target as HTMLFormElement
    const queryInput = form?.elements.namedItem('query') as HTMLInputElement
    
    if (!queryInput) return
    
    fetch(`${import.meta.env.VITE_API_URL}/chat-message`, {
        method: "POST",
        body: JSON.stringify({
            "chat_id": route.params.id ?? null,
            "model_id": 1,
            "parent_id": null,
            "message": queryInput.value
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
            <ChatMessage v-for="message in chat.messages" class="chat-message" :message="message" />
        </div>

        <div id="chat-input">
            <form @submit.prevent="sendMessage">
                <input type="text" name="query" placeholder="Enter message.." />
            </form>
        </div>
    </div>
</template>

<style scoped>
.chat {
    flex: 1;
    background: #fff;
    position: relative;
    padding-bottom: 20px;
    background: #ccc;
    height: 100%; /* Ensure chat takes full height of its parent */
    display: flex; /* Make chat a flex container */
    flex-direction: column; /* Stack children vertically */
}
#chat-messages {
    overflow-y: scroll;
    max-height: calc(100vh - 0px);
    padding: 10px;
}
#chat-input {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 100px;
    background: #666
}
    #chat-input input {
        width: 100%;
        padding:10px;
    }

</style>