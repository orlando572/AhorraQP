<template>
  <div class="search-bar-container">
    <div class="search-box">
      <input
        v-model="query"
        @input="onSearch"
        @keyup.enter="handleEnter"
        type="text"
        placeholder="Busca arroz, leche, aceite..."
        class="search-input"
      />
      <button @click="clearSearch" v-if="query" class="btn-clear">✕</button>
    </div>
    
    <div v-if="suggestions.length > 0" class="suggestions">
      <div
        v-for="suggestion in suggestions"
        :key="suggestion"
        @click="selectSuggestion(suggestion)"
        class="suggestion-item"
      >
        {{ suggestion }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['search', 'clear'])

const query = ref('')
const suggestions = ref([])

const onSearch = () => {
  if (query.value.length >= 2) {
    emit('search', query.value)
    // Aquí podrías agregar lógica de sugerencias
  }
}

const handleEnter = () => {
  emit('search', query.value)
}

const clearSearch = () => {
  query.value = ''
  suggestions.value = []
  emit('clear')
}

const selectSuggestion = (suggestion) => {
  query.value = suggestion
  emit('search', suggestion)
  suggestions.value = []
}
</script>

<style scoped>
.search-bar-container {
  position: relative;
}

.search-box {
  display: flex;
  gap: 10px;
  background: white;
  border-radius: 8px;
  padding: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.search-input {
  flex: 1;
  border: none;
  padding: 12px 16px;
  font-size: 16px;
  border-radius: 4px;
}

.search-input:focus {
  outline: none;
}

.btn-clear {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
  padding: 8px 16px;
  color: #999;
}

.suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e0e0e0;
  border-top: none;
  border-radius: 0 0 8px 8px;
  max-height: 300px;
  overflow-y: auto;
  z-index: 10;
}

.suggestion-item {
  padding: 12px 16px;
  cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
}

.suggestion-item:hover {
  background: #f5f5f5;
}
</style>