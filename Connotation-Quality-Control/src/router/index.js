import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/components/HomePage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage
    },
    {
      path: '/subtable',
      name: 'subtable',
      component: () => import('../components/panels/nhzk/IndexPage.vue')
    },{
        path: '/two',
        name: 'two',
        component:()=> import('../components/panels/nhzk/UpLoadData.vue')
    },{
      path: '/three',
      name: 'three',
      component:()=> import('../components/panels/sygyh/DefineShow.vue')
    },
    {
      path: '/four',
      name: 'four',
      component:()=> import('../components/panels/sygyh/SyDefine.vue')
    }
  ]
})

export default router
