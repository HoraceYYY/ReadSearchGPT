import { createRouter, createWebHistory } from 'vue-router'
import NewSearch from '../views/NewSearch.vue'
import MySearch from '../views/MySearch.vue'
import Tutorial from '../views/Tutorial.vue'
import Feedback from '../views/Feedback.vue'
import Terms from '../views/Terms.vue'
import Privacy from '../views/Privacy.vue'  
import Query from '../views/Query.vue'
import Searching from '../views/Searching.vue'
import SearchPreference from '../views/SearchPreference.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/preference/:searchqueries?/:apikey?',
      name: 'SearchPreference',
      component: SearchPreference,
      props: true
    },
    {
      path: '/mysearch',
      name: 'Find My Search',
      component: MySearch
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      //component: () => import('../views/AboutView.vue')
    },
    {
      path: '/tutorial', 
      name: 'Find My Tutorial',
      component: Tutorial 
    },
    {
      path: '/feedback', 
      name: 'Provide Feedback',
      component: Feedback 
    },
    {
      path: '/terms', 
      name: 'Terms',
      component: Terms 
    },
    {
      path: '/privacy', 
      name: 'Privacy',
      component: Privacy 
    },
    {
      path: '/', 
      name: 'Query',
      component: Query 
    },
    {
      path: '/searching', 
      name: 'Searching',
      component: Searching 
    },
    
  ]
})

export default router
