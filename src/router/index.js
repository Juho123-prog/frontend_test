import { createRouter, createWebHistory } from 'vue-router'
import DEF from '@/views/def.vue'
import A from '@/views/A.vue'
import B from '@/views/B.vue'
import C from '@/views/C.vue'
import D from '@/views/D.vue'
import E from '@/views/E.vue'



const routes = [
  {
    path: '/',
    redirect: '/def',
  },
  {
    path: '/def',
    component: DEF,
  },
  {
    path: '/a',
    component: A,
  },
  {
    path: '/b',
    component: B,
  },
  {
    path: '/c',
    component: C,
  },
  {
    path: '/d',
    component: D,
  },
  {
    path: '/e',
    component: E,
  },
]

const router = createRouter({
  history: createWebHistory('/juhotest/'),
  routes,
})

export default router
