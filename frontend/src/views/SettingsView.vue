<script setup lang="ts">
import { useAppStore } from '@/stores/app'
import type { ProviderInfo } from '@/types'

const appStore = useAppStore()

const providers: ProviderInfo[] = [
  { id: 'ollama', name: 'Ollama', description: '本地模型，免费离线使用', needsKey: false },
  { id: 'dashscope', name: '通义千问', description: '阿里云 DashScope API', needsKey: true },
  { id: 'openai', name: 'OpenAI', description: 'GPT-4o 及兼容接口', needsKey: true },
  { id: 'gemini', name: 'Gemini', description: 'Google Gemini 2.5', needsKey: true },
  { id: 'deepseek', name: 'DeepSeek', description: 'DeepSeek 云端 API', needsKey: true },
  { id: 'custom', name: '自定义', description: '任意 OpenAI 兼容 API', needsKey: true },
]

function selectProvider(id: ProviderInfo['id']) {
  appStore.setProvider(id)
}
</script>

<template>
  <div class="settings-view">
    <h1 class="settings-title">设置</h1>

    <section class="settings-section">
      <h2 class="section-title">模型提供方</h2>
      <p class="section-desc">选择 AI 模型后端，需在 <code>.env</code> 中配置对应的 API Key</p>
      <div class="provider-grid">
        <button
          v-for="p in providers"
          :key="p.id"
          :class="['provider-card', { active: appStore.provider === p.id }]"
          @click="selectProvider(p.id)"
        >
          <div class="provider-name">{{ p.name }}</div>
          <div class="provider-desc">{{ p.description }}</div>
          <div class="provider-tag" :class="{ free: !p.needsKey }">
            {{ p.needsKey ? '需 Key' : '免费' }}
          </div>
        </button>
      </div>
    </section>

    <section class="settings-section">
      <h2 class="section-title">连接状态</h2>
      <div class="status-card">
        <span class="status-indicator" :class="{ connected: appStore.apiConnected }" />
        <span>API 后端 {{ appStore.apiConnected ? '已连接' : '未连接' }}</span>
      </div>
    </section>

    <section class="settings-section">
      <h2 class="section-title">关于</h2>
      <div class="about-card">
        <p><strong>AI Worker</strong> — 基于 AgentScope 的智能研究助手</p>
        <p class="about-tech">Tauri 2.0 · Vue 3 · Pinia · Vite · TypeScript</p>
      </div>
    </section>
  </div>
</template>

<style scoped>
.settings-view {
  height: 100vh;
  overflow-y: auto;
  padding: 36px 40px;
}

.settings-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 28px;
}

.settings-section {
  margin-bottom: 32px;
}

.section-title {
  font-size: var(--font-lg);
  font-weight: 600;
  margin-bottom: 6px;
}

.section-desc {
  font-size: var(--font-sm);
  color: var(--text-secondary);
  margin-bottom: 14px;
}

.section-desc code {
  font-size: var(--font-xs);
}

.provider-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}

.provider-card {
  padding: 16px;
  border: 1.5px solid var(--border-light);
  border-radius: var(--radius-md);
  background: var(--bg-primary);
  text-align: left;
  transition: all 0.2s;
}

.provider-card:hover {
  border-color: var(--border-color);
  box-shadow: var(--shadow-sm);
}

.provider-card.active {
  border-color: var(--accent);
  background: var(--accent-light);
}

.provider-name {
  font-weight: 600;
  font-size: var(--font-base);
  margin-bottom: 4px;
  color: var(--text-primary);
}

.provider-desc {
  font-size: var(--font-sm);
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.provider-tag {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 10px;
  font-size: var(--font-xs);
  font-weight: 500;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
}

.provider-tag.free {
  background: #e8f5e9;
  color: #2e7d32;
}

.status-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 18px;
  background: var(--bg-secondary);
  border-radius: var(--radius-sm);
  font-size: var(--font-base);
}

.status-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--text-tertiary);
  flex-shrink: 0;
}

.status-indicator.connected {
  background: #2e7d32;
}

.about-card {
  padding: 16px 20px;
  background: var(--bg-secondary);
  border-radius: var(--radius-sm);
}

.about-tech {
  font-size: var(--font-sm);
  color: var(--text-tertiary);
  margin-top: 6px;
}
</style>
