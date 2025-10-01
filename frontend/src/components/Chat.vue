<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useEventStore, type EventData, type EventHandler } from '@/stores/eventStore'
import router from '@/router'

const route = useRoute()
const eventStore = useEventStore()

const chat = ref({})

const eventStreamHandler = (e: EventData) => {   
    if (e.type === "chat:completion") {
        const {chat_id, message_id, content, status } = e.body

        console.log(e.body)

        const chatMessageId = `chat-message-${message_id}`
        // let chatMessage = document.getElementById(chatMessageId)

        // if (! chatMessage) {
        //     chatMessage = document.createElement("div")
        //     chatMessage.id = chatMessageId
        //     chatMessage.classList.add("chat-message")
        //     document.getElementById("chat-messages")?.appendChild(chatMessage)
        // }

        // chatMessage.textContent = content

        // router.push({name: 'chat', params: { id: chat_id}})

        // if (status === "generating") {}
    }
}

const sendMessage = (submitEvent: Event) => {
    const form = submitEvent.target as HTMLFormElement
    const queryInput = form?.elements.namedItem('query') as HTMLInputElement
    
    if (!queryInput) return
    
    fetch(`${import.meta.env.VITE_API_URL}/chat-message`, {
        method: "POST",
        body: JSON.stringify({
            "chat_id": route.params.id,
            "model_id": 1,
            "parent_id": null,
            "message": queryInput.value
        }),
        headers: {"Content-Type": "application/json"}
    })
    .then((response) => response.json())
    .then((data) => {
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
    loadChat(chatId)
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
          <div v-for="message in chat.messages" class="chat-message" :class="{'is-user': message.role == 'user'}" >
            MSG: {{ message.message }}
          </div>
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
}
.chat-message {
    margin: 10px;
    background: #fff
}
    .chat-message.is-user {
        background: #ccc;
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