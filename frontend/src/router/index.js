import { createRouter, createWebHashHistory } from 'vue-router';
import HomePage from '@/components/Home.vue';

const routes = [
  {
    path: '/',
    redirect: '/home'  // 访问 / 时重定向到测试页面
  },
  {
    path: '/home',
    name: 'HomePage',
    component: HomePage
  }
];

const router = createRouter({
  history: createWebHashHistory(), // 哈希模式，路径带 #
  routes
});

export default router;