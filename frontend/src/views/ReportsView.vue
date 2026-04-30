<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchReports, fetchReportContent } from '@/api/agent'
import MessageContent from '@/components/chat/MessageContent.vue'

const reports = ref<string[]>([])
const loading = ref(true)
const activeReport = ref<string>('')
const activeContent = ref<string>('')

onMounted(async () => {
  try {
    const data = await fetchReports()
    reports.value = data.reports
  } catch {
    reports.value = []
  } finally {
    loading.value = false
  }
})

async function viewReport(filename: string) {
  activeReport.value = filename
  try {
    activeContent.value = await fetchReportContent(filename)
  } catch {
    activeContent.value = '加载报告失败'
  }
}
</script>

<template>
  <div class="reports-view">
    <div class="reports-sidebar">
      <div class="reports-sidebar-header">
        <h2 class="sidebar-title">研究报告</h2>
        <span class="report-count">{{ reports.length }} 份</span>
      </div>

      <div v-if="loading" class="loading">加载中…</div>
      <div v-else-if="reports.length === 0" class="empty">
        <p class="empty-text">暂无研究报告</p>
        <p class="empty-hint">返回对话页面，向 Friday 提出研究问题</p>
      </div>
      <div v-else class="report-list">
        <button
          v-for="r in reports"
          :key="r"
          :class="['report-item', { active: activeReport === r }]"
          @click="viewReport(r)"
        >
          <span class="report-icon">📄</span>
          <span class="report-name">{{ r }}</span>
        </button>
      </div>
    </div>

    <div class="reports-content">
      <div v-if="!activeReport" class="no-selection">
        <span class="no-selection-icon">📋</span>
        <p>选择左侧报告查看内容</p>
      </div>
      <div v-else class="report-preview">
        <MessageContent :content="activeContent" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.reports-view {
  display: flex;
  height: 100vh;
}

.reports-sidebar {
  width: 280px;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-light);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.reports-sidebar-header {
  padding: 20px 18px 14px;
  border-bottom: 1px solid var(--border-light);
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}

.sidebar-title {
  font-size: var(--font-lg);
  font-weight: 600;
}

.report-count {
  font-size: var(--font-xs);
  color: var(--text-tertiary);
}

.report-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.report-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  font-size: var(--font-sm);
  color: var(--text-secondary);
  text-align: left;
  transition: all 0.15s;
  width: 100%;
}

.report-item:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.report-item.active {
  background: var(--accent-light);
  color: var(--accent);
  font-weight: 500;
}

.report-icon {
  font-size: 16px;
  flex-shrink: 0;
}

.report-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.reports-content {
  flex: 1;
  overflow-y: auto;
  padding: 32px 40px;
}

.no-selection {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 12px;
  color: var(--text-tertiary);
  font-size: var(--font-base);
}

.no-selection-icon {
  font-size: 40px;
}

.report-preview {
  max-width: 800px;
}

.loading, .empty {
  padding: 24px;
  text-align: center;
}

.empty-text {
  font-size: var(--font-base);
  color: var(--text-secondary);
  margin-bottom: 6px;
}

.empty-hint {
  font-size: var(--font-sm);
  color: var(--text-tertiary);
}
</style>
