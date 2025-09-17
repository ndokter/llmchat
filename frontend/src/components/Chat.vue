<script setup lang="ts">
const sendMessage = (submitEvent: Event) => {
    console.log(submitEvent.target.elements.query.value)
}
</script>

<template>
    <div class="chat">
        <form @submit.prevent="sendMessage">
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