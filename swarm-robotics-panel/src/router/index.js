import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../components/LoginPage.vue';
import MainDashboard from '../components/MainDashboard.vue';
import PythonCode from '../components/PythonCode.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: LoginPage,
      meta: { requiresAuth: false }
    },
    {
      path: '/',
      name: 'MainDashboard',
      component: MainDashboard,
      meta: { requiresAuth: true }
    },
    {
      path: '/python-code',
      name: 'PythonCode',
      component: PythonCode,
      meta: { requiresAuth: true }
    }
  ]
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('access_token');
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router;
