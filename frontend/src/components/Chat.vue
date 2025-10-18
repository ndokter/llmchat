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

            <div id="chat-input">
                <form @submit.prevent="sendMessage">
                    <textarea 
                        name="query"
                        placeholder="Enter message.." 
                        rows="1"
                    ></textarea>
                    <button class="send-button">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                        <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </button>

                </form>
            </div>
    </div>
</template>

<style scoped>
.chat {
    flex: 1;
    background: #fff;
    position: relative;
    /* padding-bottom: 100px; */
    height: 100%;
    display: flex;
    flex-direction: column;
    margin-left: 50px;
    margin-right: 50px;
}
#chat-messages {
    overflow-y: scroll;
    max-height: calc(100vh - 0px);
    padding: 10px 0 100px 0;
}

#chat-input {
    display: flex;
    align-items: flex-end;
    padding: 12px 10px;
    border: 1px solid #e5e7eb;
    border-radius: .75rem;
    background: white;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    transition: box-shadow 0.2s ease;
    position: absolute;
    bottom: 15px;
    left: 15px;
    right: 15px;
}
    #chat-input textarea {
        flex: 1;
        border: none;
        outline: none;
        resize: none;
        font-size: 16px;
        line-height: 1.5;
        max-height: 200px;
        overflow-y: auto;
    }

    #chat-input textarea::placeholder {
        color: #9ca3af;
    }
</style>