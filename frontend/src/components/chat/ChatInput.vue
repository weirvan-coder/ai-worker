<script setup lang="ts">
import { ref, computed } from 'vue'

const emit = defineEmits<{
  send: [content: string]
}>()

const input = ref('')
const textareaRef = ref<HTMLTextAreaElement>()

const canSend = computed(() => input.value.trim().length > 0)

function handleSend() {
  const text = input.value.trim()
  if (!text) return
  emit('send', text)
  input.value = ''
  textareaRef.value?.focus()
}

function handleEnter(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSend()
  }
}

function autoResize() {
  const el = textareaRef.value
  if (!el) return
  el.style.height = 'auto'
  el.style.height = Math.min(el.scrollHeight, 160) + 'px'
}
</script>

<template>
  <div class="input-float-wrapper">
    <div class="input-float-container">
      <textarea
        ref="textareaRef"
        v-model="input"
        class="input-textarea"
        :placeholder="'输入研究问题…  Enter 发送，Shift+Enter 换行'"
        rows="1"
        @keydown="handleEnter"
        @input="autoResize"
      />
      <button
        class="send-btn"
        :disabled="!canSend"
        :class="{ active: canSend }"
        @click="handleSend"
      >
        ↑
      </button>
    </div>
  </div>
</template>

<style scoped>
.input-float-wrapper {
  padding: 20px 24px 28px;
  display: flex;
  justify-content: center;
  flex-shrink: 0;
  background: linear-gradient(180deg, transparent 0%, var(--bg-primary) 40%);
  position: relative;
  z-index: 10;
}

.input-float-container {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  width: 100%;
  max-width: 760px;
  background: var(--bg-primary);
  border: 1.5px solid var(--border-color);
  border-radius: var(--radius-xl);
  padding: 10px 12px 10px 18px;
  box-shadow: var(--shadow-input);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.input-float-container:focus-within {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-light), var(--shadow-input);
}

.input-textarea {
  flex: 1;
  font-size: var(--font-base);
  color: var(--text-primary);
  line-height: 1.55;
  resize: none;
  min-height: 24px;
  max-height: 160px;
}

.input-textarea::placeholder {
  color: var(--text-tertiary);
}

.send-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--bg-tertiary);
  color: var(--text-tertiary);
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.2s;
}

.send-btn.active {
  background: var(--accent);
  color: #fff;
}

.send-btn.active:hover {
  background: var(--accent-hover);
  transform: scale(1.05);
}

.send-btn:disabled {
  cursor: default;
}
</style>
