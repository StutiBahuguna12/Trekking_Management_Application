import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Register from '@/views/Register.vue'
import Login from '@/views/Login.vue'
import Admin_dashboard  from '@/views/Admin_dashboard.vue'
import Trek_staff_dashboard from '@/views/Trek_staff_dashboard.vue'
import Trekker_dashboard from '@/views/Trekker_dashboard.vue'




const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
   {path: '/register',component:Register},
   {path: '/login', component:Login},
   {path:'/',component:Home},
   {path:'/admin_dashboard',componet:Admin_dashboard},
   {path:'/trekker_dashboard',component:Trekker_dashboard},
   {path:'trek_staff_dashboard',component:Trek_staff_dashboard}
  
   
  ],
})

export default router
