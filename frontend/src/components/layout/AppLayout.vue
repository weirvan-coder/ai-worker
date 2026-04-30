<script setup lang="ts">
import { computed } from 'vue'
import { useAppStore } from '@/stores/app'
import AppSidebar from './AppSidebar.vue'

const appStore = useAppStore()

const mainStyle = computed(() => ({
  marginLeft: appStore.sidebarCollapsed
    ? 'var(--sidebar-collapsed-width)'
    : 'var(--sidebar-width)',
}))
</script>

<template>
  <div class="app-layout">
    <AppSidebar />
    <main :style="mainStyle" class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<style scoped>
.app-layout {
  height: 100vh;
  display: flex;
}

.main-content {
  flex: 1;
  height: 100vh;
  overflow: hidden;
  transition: margin-left var(--transition);
  display: flex;
  flex-direction: column;
}
</style>
