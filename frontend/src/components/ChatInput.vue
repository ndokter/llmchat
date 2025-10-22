<script setup lang="ts">
import { useModelsStore } from '@/stores/modelStore'
import { onMounted, ref, watch } from 'vue'

const emit = defineEmits(['submit'])

const modelsStore = useModelsStore()
const query = ref('')
const selectedModel = ref()

onMounted(() => {
  if (modelsStore.models.length === 0) {
    modelsStore.fetchModels()
  }
})

watch(() => modelsStore.models, (newModels) => {
  if (newModels.length > 0 && !selectedModel.value) {
    selectedModel.value = newModels[0].id
  }
})

const handleSubmit = (e: Event) => {
  e.preventDefault()
  console.log({ query: query.value, model: selectedModel.value })
  if (query.value.trim()) {
    emit('submit', { query: query.value, model: selectedModel.value })
    query.value = ''
  }
}
const handleInput = (e: Event) => {
  const target = e.target as HTMLTextAreaElement
  if (!target) return

  // Text area vertical resizing
  target.style.height = 'auto';
  target.style.height = Math.min(target.scrollHeight, 450) + 'px';
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
          <select v-model="selectedModel" id="model-select" name="model">
            <option 
            v-for="modelItem in modelsStore.models" 
            :key="modelItem.id" 
            :value="modelItem.id"
            >{{ modelItem.alias || modelItem.name }}</option>
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