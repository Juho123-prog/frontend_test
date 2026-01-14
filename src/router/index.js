import { createRouter, createWebHistory } from 'vue-router'
import DEF from '@/views/def.vue'
import A from '@/views/A.vue'
import B from '@/views/B.vue'
import C from '@/views/C.vue'
import D from '@/views/D.vue'



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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router