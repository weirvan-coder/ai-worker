<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import { useChatStore } from '@/stores/chat'
import { sendMessage, healthCheck } from '@/api/agent'
import { useAppStore } from '@/stores/app'
import ChatMessage from '@/components/chat/ChatMessage.vue'
import ChatInput from '@/components/chat/ChatInput.vue'

const chatStore = useChatStore()
const appStore = useAppStore()
const messagesEl = ref<HTMLDivElement>()

async function handleSend(content: string) {
  chatStore.addUserMessage(content)
  chatStore.isResponding = true
  chatStore.setError('')
  const streamId = chatStore.addAssistantPlaceholder()

  await nextTick()
  scrollToBottom()

  try {
    await sendMessage(content, (chunk) => {
      chatStore.appendToMessage(streamId, chunk)
      scrollToBottom()
    })
    chatStore.finishStreaming(streamId)
  } catch (err: any) {
    chatStore.setError(err.message || '请求失败')
  } finally {
    chatStore.isResponding = false
    checkHealth()
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesEl.value) {
      messagesEl.value.scrollTop = messagesEl.value.scrollHeight
    }
  })
}

async function checkHealth() {
  const result = await healthCheck()
  appStore.setApiConnected(result.ok && result.ready)
}

checkHealth()
</script>

<template>
  <div class="home-view">
    <div class="chat-area">
      <div v-if="chatStore.messages.length === 0" class="welcome">
        <div class="welcome-icon">◈</div>
        <h1 class="welcome-title">Friday 研究助手</h1>
        <p class="welcome-desc">我可以帮你搜索网络、分析信息并生成研究报告</p>
        <div class="welcome-hints">
          <button
            v-for="hint in [
              '帮我研究一下人工智能的最新发展趋势',
              '总结 Claude 4 的核心新功能',
              '比较 DeepSeek 和 GPT 的差异',
            ]"
            :key="hint"
            class="hint-chip"
            @click="handleSend(hint)"
          >
            {{ hint }}
          </button>
        </div>
      </div>

      <div v-else ref="messagesEl" class="messages-list">
        <ChatMessage
          v-for="msg in chatStore.messages"
          :key="msg.id"
          :message="msg"
        />
        <div v-if="chatStore.error" class="error-msg">
          ⚠️ {{ chatStore.error }}
        </div>
      </div>
    </div>

    <ChatInput @send="handleSend" />
  </div>
</template>

<style scoped>
.home-view {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--bg-primary);
}

.chat-area {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.welcome {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 40px;
  text-align: center;
}

.welcome-icon {
  font-size: 48px;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.welcome-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.welcome-desc {
  font-size: var(--font-lg);
  color: var(--text-secondary);
  max-width: 480px;
  margin: 0 0 16px;
}

.welcome-hints {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  max-width: 600px;
}

.hint-chip {
  padding: 10px 18px;
  background: var(--bg-secondary);
  color: var(--text-secondary);
  border-radius: 20px;
  font-size: var(--font-sm);
  transition: all 0.2s;
}

.hint-chip:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.messages-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px 24px;
  scroll-behavior: smooth;
}

.error-msg {
  padding: 12px 16px;
  margin: 8px auto;
  max-width: 760px;
  background: #fff0f0;
  color: #c62828;
  border-radius: var(--radius-sm);
  font-size: var(--font-sm);
}
</style>
