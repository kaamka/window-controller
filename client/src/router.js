import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Settings from './views/settings.vue'
import Offline from './views/offline.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/offline',
      name: 'offline',
      component: Offline
    },
    {
      path: '/settings',
      name: 'settings',
      component: Settings
    }
  ]
})
