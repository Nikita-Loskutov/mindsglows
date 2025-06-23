import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    
    {
      path: '/',
      name: 'main',
      component: () => import('../views/HomeView.vue'),
    },
    {
      path: '/mine',
      name: 'upgrade',
      component: () => import('../views/MineView.vue'),
    },
    {
      path: '/friends',
      name: 'friend',
      component: () => import('../views/FriendsView.vue'),
    },
    {
      path: '/earn',
      name: 'earn',
      component: () => import('../views/TasksView.vue'),
    },
    {
      path: '/airdrop',
      name: 'airdrop',
      component: () => import('../views/AirdropView.vue'),
    }
  ],
})

export default router
