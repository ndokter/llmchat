<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useEventStore, type EventData, type EventHandler } from '@/stores/eventStore'
import router from '@/router'
import markdownit from 'markdown-it'
import hljs from 'highlight.js'

const props = defineProps(['message'])

const md = markdownit({
  highlight: function (str: any, lang: any) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return '<pre><code class="hljs">' +
               hljs.highlight(str, { language: lang, ignoreIllegals: true }).value +
               '</code></pre>';
      } catch (__) {}
    }

    return '<pre><code class="hljs">' + md.utils.escapeHtml(str) + '</code></pre>';
  }
});
const markdownMessage = computed(() => {
    return md.render(props.message.message)
})

onMounted(() => {

})

onUnmounted(() => {

})


</script>

<template>
    <div v-html="markdownMessage" :class="{'is-user': props.message.role == 'user'}" class="markdown-body"></div>
</template>

<style scoped>
.chat-message {
    margin: 10px;
    padding: 10px;
    background: #fff;
}
.chat-message.is-user {
    background: #ccc;
}
</style>