<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { useEventStore, type EventData, type EventHandler } from '@/stores/eventStore'

const eventStore = useEventStore()

const eventStreamHandler = (e: EventData) => {   
    if (e.type === "chat:completion") {
        const {chat_id, message_id, content, status } = e.body

        console.log(e.body)

        const chatMessageId = `chat-message-${message_id}`
        let chatMessage = document.getElementById(chatMessageId)

        if (! chatMessage) {
            chatMessage = document.createElement("div")
            chatMessage.id = chatMessageId
            chatMessage.classList.add("chat-message")
            document.getElementById("chat-messages")?.appendChild(chatMessage)
        }

        chatMessage.textContent = content

        // if (status === "generating") {}
    }
}

const addMessage = (submitEvent: Event) => {
    const form = submitEvent.target as HTMLFormElement
    const queryInput = form?.elements.namedItem('query') as HTMLInputElement
    
    if (!queryInput) return
    
    fetch(`${import.meta.env.VITE_API_URL}/chat-message`, {
        method: "POST",
        body: JSON.stringify({
            "chat_id": null,
            "model_id": 2,
            "parent_id": null,
            "message": queryInput.value
        }),
        headers: {"Content-Type": "application/json"}
    })
}

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

        </div>

        <div id="chat-input">
            <form @submit.prevent="addMessage">
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