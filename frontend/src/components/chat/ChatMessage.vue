<script setup lang="ts">
import type { ChatMessage } from '@/types'
import MessageContent from './MessageContent.vue'

defineProps<{
  message: ChatMessage
}>()

function formatTime(ts: number): string {
  return new Date(ts).toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

<template>
  <div :class="['msg-wrapper', message.role]">
    <div class="msg-avatar">
      {{ message.role === 'user' ? '🧑' : '🤖' }}
    </div>
    <div class="msg-body">
      <div class="msg-meta">
        <span class="msg-role">{{ message.role === 'user' ? '我' : 'Friday' }}</span>
        <span class="msg-time">{{ formatTime(message.timestamp) }}</span>
      </div>
      <div class="msg-content">
        <MessageContent
          :content="message.content"
          :is-streaming="message.isStreaming"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.msg-wrapper {
  display: flex;
  gap: 14px;
  padding: 16px 0;
  max-width: 820px;
  margin: 0 auto;
  width: 100%;
  transition: background 0.2s;
  border-radius: var(--radius-md);
}

.msg-wrapper.user {
  padding-left: 0;
}

.msg-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
  user-select: none;
}

.msg-body {
  flex: 1;
  min-width: 0;
}

.msg-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}

.msg-role {
  font-weight: 600;
  font-size: var(--font-sm);
  color: var(--text-primary);
}

.msg-time {
  font-size: var(--font-xs);
  color: var(--text-tertiary);
}

.msg-content {
  color: var(--text-primary);
  font-size: var(--font-base);
}
</style>
