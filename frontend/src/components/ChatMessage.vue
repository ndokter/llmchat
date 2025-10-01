<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useEventStore, type EventData, type EventHandler } from '@/stores/eventStore'
import router from '@/router'

const props = defineProps(['message'])

onMounted(() => {

})

onUnmounted(() => {

})


</script>

<template>
    {{ props.message.message }}
</template>

<style scoped>

</style>