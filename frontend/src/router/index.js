// src/router/index.js
import { createRouter, createWebHashHistory } from 'vue-router';
import TestBackend from '@/views/TestBackend.vue';

const routes = [
  {
    path: '/',
    redirect: '/test-backend'  // 访问 / 时重定向到测试页面
  },
  {
    path: '/test-backend',
    name: 'TestBackend',
    component: TestBackend
  }
];

const router = createRouter({
  history: createWebHashHistory(), // 哈希模式，路径带 #
  routes
});

export default router;