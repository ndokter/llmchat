<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits(['submit'])

const query = ref('')
const model = ref('Llama 3.2')

const handleSubmit = (e: Event) => {
  e.preventDefault()
  if (query.value.trim()) {
    emit('submit', { query: query.value, model: model.value })
    query.value = ''
  }
}
const handleInput = (e: Event) => {
  const textarea = e.target

  if (!textarea) return

  // Text area vertical resizing
  textarea.addEventListener('input', function() {
  textarea.style.height = 'auto';
  textarea.style.height = Math.min(textarea.scrollHeight, 450) + 'px';
  });
}
</script>

<template>
  <div id="chat-input">
    <form @submit="handleSubmit">
      <div class="textarea-container">
        <textarea
          v-model="query"
          name="query"
          placeholder="Enter message.."
          rows="1"
          @input="handleInput"
        ></textarea>
      </div>
      <div class="actions">
        <span class="action">
          <select v-model="model" id="model-select" name="model">
            <option value="Llama 3.2">Llama 3.2</option>
            <option value="Chat GPT 5">Chat GPT 5</option>
            <option value="Gemini 2.5 Flash">Gemini 2.5 Flash</option>
          </select>           
        </span>    
        <span class="action">
          <button type="submit" class="send-button">send</button>
        </span>
      </div>
    </form>
  </div>
</template>

<style scoped>
#chat-input {
  display: flex;
  flex-direction: column;
  padding: 10px 10px 2px 10px;
  outline: 1px solid #d8d8d8;
  border-radius: .75rem;
  background: white;
  box-shadow: 1px 2px 3px rgba(80, 80, 80, 0.05);
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
  /* max-height: 300px; */
  overflow-y: auto;
  width: 100%;
}
.actions {
  width: 100%;
  padding: 8px 0;
  color: #6b7280;
  font-size: 14px;
  display: inline-block;
}
.action {
  margin-right: 10px;
}
#chat-input textarea::placeholder {
  color: #9ca3af;
}
</style>