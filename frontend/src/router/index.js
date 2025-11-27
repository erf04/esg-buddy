import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import Chat from '@/components/Chat.vue';
import LoginSignup from '@/components/LoginSignup.vue';

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginSignup },
  { path: '/signup', component: LoginSignup },
  { path: '/chat', component: Chat, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login');
  } else if ((to.path === '/login' || to.path === '/signup') && authStore.isAuthenticated) {
    next('/chat');
  } else {
    next();
  }
});

export default router;