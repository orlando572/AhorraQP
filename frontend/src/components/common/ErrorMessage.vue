<template>
  <div v-if="show" class="error-message" :class="type">
    <span>{{ message }}</span>
    <button @click="close" class="close-btn">✕</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  message: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'error' // 'error', 'warning', 'success'
  },
  duration: {
    type: Number,
    default: 5000
  }
})

const show = ref(true)

const close = () => {
  show.value = false
}

if (props.duration > 0) {
  setTimeout(() => {
    show.value = false
  }, props.duration)
}
</script>

<style scoped>
.error-message {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  animation: slideIn 0.3s ease-in;
}

@keyframes slideIn {
  from {
    transform: translateX(-100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.error-message.error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.error-message.warning {
  background: #fff3cd;
  color: #856404;
  border: 1px solid #ffeeba;
}

.error-message.success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
  opacity: 0.7;
}

.close-btn:hover {
  opacity: 1;
}
</style>