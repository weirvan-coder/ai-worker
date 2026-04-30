<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAppStore } from '@/stores/app'
import type { NavItem } from '@/types'

const router = useRouter()
const route = useRoute()
const appStore = useAppStore()

const navItems: NavItem[] = [
  { id: 'home', label: '对话', icon: '💬', route: '/' },
  { id: 'reports', label: '报告', icon: '📄', route: '/reports' },
  { id: 'settings', label: '设置', icon: '⚙', route: '/settings' },
]

const sidebarClass = computed(() => ({
  'sidebar-collapsed': appStore.sidebarCollapsed,
}))

function navigate(item: NavItem) {
  router.push(item.route)
}

const connectedDot = computed(() => (appStore.apiConnected ? '●' : '○'))
const connectedColor = computed(() => (appStore.apiConnected ? 'var(--accent)' : 'var(--text-tertiary)'))
</script>

<template>
  <aside :class="['sidebar', sidebarClass]">
    <div class="sidebar-header" @click="appStore.toggleSidebar()">
      <span class="logo-icon">◈</span>
      <span v-if="!appStore.sidebarCollapsed" class="logo-text">AI Worker</span>
    </div>

    <nav class="sidebar-nav">
      <button
        v-for="item in navItems"
        :key="item.id"
        :class="['nav-item', { active: route.path === item.route }]"
        @click="navigate(item)"
      >
        <span class="nav-icon">{{ item.icon }}</span>
        <span v-if="!appStore.sidebarCollapsed" class="nav-label">{{ item.label }}</span>
      </button>
    </nav>

    <div class="sidebar-footer">
      <div v-if="!appStore.sidebarCollapsed" class="sidebar-collapse-btn" @click="appStore.toggleSidebar()">
        <span class="collapse-icon">◂</span>
        <span>收起侧栏</span>
      </div>
      <div v-else class="sidebar-collapse-btn" @click="appStore.toggleSidebar()">
        <span class="collapse-icon expanded">▸</span>
      </div>
      <div class="status-dot" :style="{ color: connectedColor }">
        {{ connectedDot }}
        <span v-if="!appStore.sidebarCollapsed" class="status-text">API {{ appStore.apiConnected ? '已连接' : '未连接' }}</span>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: var(--sidebar-width);
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-light);
  display: flex;
  flex-direction: column;
  z-index: 100;
  transition: width var(--transition);
  user-select: none;
}

.sidebar-collapsed {
  width: var(--sidebar-collapsed-width);
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 18px;
  cursor: pointer;
  border-bottom: 1px solid var(--border-light);
}

.logo-icon {
  font-size: 24px;
  color: var(--text-primary);
  flex-shrink: 0;
}

.logo-text {
  font-size: var(--font-lg);
  font-weight: 700;
  color: var(--text-primary);
  white-space: nowrap;
}

.sidebar-nav {
  flex: 1;
  padding: 12px 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 14px;
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--text-secondary);
  font-size: var(--font-base);
  font-weight: 500;
  transition: all 0.15s ease;
  width: 100%;
  text-align: left;
  white-space: nowrap;
}

.nav-item:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.nav-item.active {
  background: var(--accent-light);
  color: var(--accent);
  font-weight: 600;
}

.nav-icon {
  font-size: 18px;
  flex-shrink: 0;
  width: 24px;
  text-align: center;
}

.nav-label {
  overflow: hidden;
}

.sidebar-footer {
  padding: 12px 8px;
  border-top: 1px solid var(--border-light);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.sidebar-collapse-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  cursor: pointer;
  color: var(--text-tertiary);
  font-size: var(--font-sm);
  border-radius: var(--radius-sm);
  transition: background 0.15s;
}

.sidebar-collapse-btn:hover {
  background: var(--bg-hover);
}

.collapse-icon {
  font-size: 14px;
  width: 24px;
  text-align: center;
}

.status-dot {
  padding: 4px 14px;
  font-size: var(--font-xs);
  color: var(--text-tertiary);
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-text {
  white-space: nowrap;
}
</style>
