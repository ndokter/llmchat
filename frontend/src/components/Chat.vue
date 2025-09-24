<script setup lang="ts">
const addMessage = (submitEvent: Event) => {
    console.log(submitEvent.target.elements.query.value)

    console.log(import.meta.env.VITE_API_URL)
    fetch(`${import.meta.env.VITE_API_URL}/chat-message`, {
        method: "POST",
        body: JSON.stringify({
            "chat_id": null,
            "model_id": 2,
            "parent_id": null,
            "message": submitEvent.target.elements.query.value
        }),
        headers: {"Content-Type": "application/json"}
    })
}
</script>

<template>
    <div class="chat">
        <form @submit.prevent="addMessage">
            <input type="text" name="query" />
        </form>
    </div>
</template>

<style scoped>
.chat {
    flex: 1;
    padding: 1rem;
    background: #fff;
}
</style>