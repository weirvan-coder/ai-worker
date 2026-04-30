import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { ChatMessage } from '@/types'

export const useChatStore = defineStore('chat', () => {
  const messages = ref<ChatMessage[]>([])
  const isResponding = ref(false)
  const error = ref<string | null>(null)

  const lastAssistantMessage = computed(() => {
    for (let i = messages.value.length - 1; i >= 0; i--) {
      if (messages.value[i].role === 'assistant') return messages.value[i]
    }
    return null
  })

  function addUserMessage(content: string) {
    const msg: ChatMessage = {
      id: Date.now().toString(36),
      role: 'user',
      content,
      timestamp: Date.now(),
    }
    messages.value.push(msg)
  }

  function addAssistantPlaceholder() {
    const msg: ChatMessage = {
      id: 'streaming_' + Date.now().toString(36),
      role: 'assistant',
      content: '',
      timestamp: Date.now(),
      isStreaming: true,
    }
    messages.value.push(msg)
    return msg.id
  }

  function appendToMessage(id: string, chunk: string) {
    const msg = messages.value.find((m) => m.id === id)
    if (msg) msg.content += chunk
  }

  function finishStreaming(id: string) {
    const msg = messages.value.find((m) => m.id === id)
    if (msg) msg.isStreaming = false
  }

  function clearMessages() {
    messages.value = []
    error.value = null
  }

  function setError(err: string) {
    error.value = err
  }

  return {
    messages,
    isResponding,
    error,
    lastAssistantMessage,
    addUserMessage,
    addAssistantPlaceholder,
    appendToMessage,
    finishStreaming,
    clearMessages,
    setError,
  }
})
