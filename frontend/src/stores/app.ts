import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ProviderId } from '@/types'

export const useAppStore = defineStore('app', () => {
  const sidebarCollapsed = ref(false)
  const provider = ref<ProviderId>('dashscope')
  const apiConnected = ref(false)

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  function setProvider(p: ProviderId) {
    provider.value = p
  }

  function setApiConnected(v: boolean) {
    apiConnected.value = v
  }

  return {
    sidebarCollapsed,
    provider,
    apiConnected,
    toggleSidebar,
    setProvider,
    setApiConnected,
  }
})
