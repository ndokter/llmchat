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
                <div class="textarea-container">
                    <textarea
                        name="query"
                        placeholder="Enter message.."
                        rows="1"
                    ></textarea>
                </div>
                <div class="actions">
                    <select id="fruit-select" name="fruit">
                        <option value="Llama 3.2">Llama 3.2</option>
                        <option value="Chat GPT 5">Chat GPT 5</option>
                        <option value="Gemini 2.5 Flash">Gemini 2.5 Flash</option>
                    </select>                  
                    <button class="send-button">
                        send
                        <!-- <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                        <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg> -->
                    </button>
                </div>
            </form>
        </div>
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

#chat-input {
    display: flex;
    flex-direction: column;
    padding: 5px 10px 20px 10px;
    border: 1px solid #e5e7eb;
    border-radius: .75rem;
    background: white;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    transition: box-shadow 0.2s ease;
    margin: 0 15px 15px 15px;
}
.textarea-container {
    display: flex;
    align-items: flex-end;
    width: 100%;
    margin-bottom: 10px;
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
        width: 100%;
    }
    
    .actions {
        width: 100%;
        padding: 8px 0;
        color: #6b7280;
        font-size: 14px;
    }

    #chat-input textarea::placeholder {
        color: #9ca3af;
    }

    
</style>