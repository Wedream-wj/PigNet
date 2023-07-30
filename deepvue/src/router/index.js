import { createRouter, createWebHistory } from 'vue-router'
import Layout from '../layout/Layout.vue'

// 配置路由
const routes = [
  {
    path: '/',
    name: 'Layout',
    component: Layout,
    redirect: '/yolo',
    children: [
      {
        path: 'user',
        name: 'User',
        component: ()=>import("@/views/User"),
      },
      {
        path: 'book',
        name: 'Book',
        component: ()=>import("@/views/Book"),
      },
      {
        path: 'bookClassification2',
        name: 'BookClassification2',
        component: ()=>import("@/views/BookClassification2"),
      },
      {
        path: 'news',
        name: 'News',
        component: ()=>import("@/views/News"),
      },
      {
        path: 'person',
        name: 'Person',
        component: ()=>import("@/views/Person")
      },
      {
        path: 'mavonDisplay',
        name: 'MavonDisplay',
        component: ()=>import("@/views/MavonDisplay")
      },
      {
        path: '/test',
        name: 'Test',
        component: ()=>import("@/views/Test")
      },
      {
        path: '/markdown',
        name: 'Markdown',
        component: ()=>import("@/views/Markdown")
      },
      {
        path: '/contest',
        name: 'Contest',
        component: ()=>import("@/views/Contest")
      },
      {
        path: '/yolo',
        name: 'Yolo',
        component: ()=>import("@/views/Yolo")
      },
      {
        path: 'knowledge',
        name: 'Knowledge',
        component: ()=>import("@/views/Knowledge")
      },
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: ()=>import("@/views/Login")
  },
  {
    path: '/register',
    name: 'Register',
    component: ()=>import("@/views/Register")
  },
  {
    path: '/retrievePassword',
    name: 'RetrievePassword',
    component: ()=>import("@/views/RetrievePassword")
  },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
