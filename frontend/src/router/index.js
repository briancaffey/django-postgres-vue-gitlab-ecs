import Vue from 'vue'
import Router from 'vue-router'
import store from '../store'
import Home from '@/views/Home.vue'

Vue.use(Router)

const ifNotAuthenticated = (to, from, next) => {
  if (!store.getters.isAuthenticated) {
    next();
    return;
  }
  next('/');
};

const ifAuthenticated = (to, from, next) => {
  if (store.getters.isAuthenticated) {
    next();
    return;
  }
  next('/login');
};

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/about',
      name: 'about',
      beforeEnter: ifAuthenticated,
      component: () => import(/* webpackChunkName: "about" */ '@/views/About.vue')
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
      beforeEnter: ifNotAuthenticated,
    },
    {
      path: '/sockets',
      name: 'Sockets',
      component: () => import('@/views/Sockets.vue'),
      beforeEnter: ifAuthenticated,
    },
  ]
})

export default router;