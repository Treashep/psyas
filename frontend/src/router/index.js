import { createRouter, createWebHistory } from 'vue-router';
import TestBackend from '@/views/TestBackend.vue';

const routes = [
  {
    path: '/test-backend',
    name: 'TestBackend',
    component: TestBackend
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;