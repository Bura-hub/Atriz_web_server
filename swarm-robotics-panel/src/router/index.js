import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../components/LoginPage.vue';
import MainDashboard from '../components/MainDashboard.vue';
import PythonCode from '../components/PythonCode.vue';  // Se restaura la importación de PythonCode

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginPage
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
    meta: { requiresAuth: true }  // Se asegura que esta ruta también requiera autenticación
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Guard de autenticación
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('access_token');
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router;
