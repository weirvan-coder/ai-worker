import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { title: 'Friday · 对话' },
    },
    {
      path: '/reports',
      name: 'reports',
      component: () => import('@/views/ReportsView.vue'),
      meta: { title: '研究报告' },
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/SettingsView.vue'),
      meta: { title: '设置' },
    },
  ],
})

router.beforeEach((to) => {
  if (to.meta.title) {
    document.title = to.meta.title as string + ' · AI Worker'
  }
})

export default router
