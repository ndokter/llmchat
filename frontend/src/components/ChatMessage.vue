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
const formatDate = (isoString: string) => {
  const now = new Date()
  const date = new Date(isoString);
  const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const startOfInputDate = new Date(date.getFullYear(), date.getMonth(), date.getDate());
  const startOfYesterday = new Date(startOfToday);
  startOfYesterday.setDate(startOfYesterday.getDate() - 1);

  const hours = date.getHours().toString().padStart(2, '0');
  const minutes = date.getMinutes().toString().padStart(2, '0');
  const formattedTime = `${hours}:${minutes}`;

  if (startOfInputDate.getTime() === startOfToday.getTime()) {
    return `today ${formattedTime}`;
  } else if (startOfInputDate.getTime() === startOfYesterday.getTime()) {
    return `yesterday at ${formattedTime}`;
  } else {
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    const year = date.getFullYear();
    const formattedDate = `${month}/${day}/${year}`;
    return `${formattedDate} at ${formattedTime}`;
  }
}

onMounted(() => {
  console.log(props.message)
})

onUnmounted(() => {

})


</script>

<template>
  <div class="chat-message">
    <div v-if="props.message.role == 'assistant'" class="top">
        <span class="title">
          {{ props.message.model.alias || props.message.model.title }}
        </span> 
        <span class="date">
          {{ formatDate(props.message.created_at) }}
        </span>
    </div>
    <div class="chat-body-container">
      <div v-html="markdownMessage" :class="props.message.role" class="chat-body markdown-body"></div>
    </div>
  </div>
</template>

<style scoped>
.chat-message {
  margin-top: 20px;
}
.chat-message .top {
  margin-left: 25px;

  .title {
    font-weight: 700;
    font-size: 18px;
  }

  .date {
    font-weight: 600;
    margin-left: 10px;
    font-size: 12px;
  }
}

.chat-body-container {
    display: grid;
}
  .chat-body {
      margin: 10px;
      padding: 10px 15px;
      background: #fff;
      border-radius: 10px;
  }
    .chat-body.user {
      background: #eeeeee;
      max-width: 70%;
      
      margin-right: 25px;
      margin-left: auto;
      justify-items: end;
    }
    .chat-body.assistant {
      padding-top: 0;
      margin-top: 0;
    }
</style>