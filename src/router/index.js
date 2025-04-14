import { createRouter, createWebHistory } from 'vue-router'
import { routes } from './routes'
import Layout from '../components/LayOut.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Layout,
      children: routes
    }
  ]
})

export default router