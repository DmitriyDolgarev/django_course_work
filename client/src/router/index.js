import { createRouter, createWebHistory } from 'vue-router'
import CarsView from '@/views/CarsView.vue'
import MarksView from '@/views/MarksView.vue'
import ClassesView from '@/views/ClassesView.vue'
import BodyTypesView from '@/views/BodyTypesView.vue'
import CountriesView from '@/views/CountriesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/", 
      name: "CarsView", 
      component: CarsView
    }, 
    {
      path: "/marks", 
      name: "MarksView", 
      component: MarksView
    }, 
    {
      path: "/classes", 
      name: "ClassesView", 
      component: ClassesView
    }, 
    {
      path: "/body-types", 
      name: "BodyTypesView", 
      component: BodyTypesView
    }, 
    {
      path: "/countries", 
      name: "CountriesView", 
      component: CountriesView
    }
  ]
})

export default router
