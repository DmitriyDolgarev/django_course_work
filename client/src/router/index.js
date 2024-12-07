import { createRouter, createWebHistory } from 'vue-router'
import CarsView from '@/views/CarsView.vue'
import MarksView from '@/views/MarksView.vue'
import ClassesView from '@/views/ClassesView.vue'
import BodyTypesView from '@/views/BodyTypesView.vue'
import CountriesView from '@/views/CountriesView.vue'
import useUserProfileStore from '@/stores/UserProfileStore'
import LoginView from '@/views/LoginView.vue'
import UserView from '@/views/UserView.vue'

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
    }, 
    {
      path: "/login", 
      name: "Login", 
      component: LoginView
    }, 
    {
      path: "/userPage", 
      name: "UserView", 
      component: UserView
    }
  ]
})

router.beforeEach(async (to, from) => {
  const userPorfileStore = useUserProfileStore()

  if (
    // make sure the user is authenticated
    !userPorfileStore.is_auth &&
    // ❗️ Avoid an infinite redirect
    to.name !== 'Login'
  ) {
    // redirect the user to the login page
    return { name: 'Login' }
  }
})

export default router
