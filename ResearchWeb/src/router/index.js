import { createRouter, createWebHistory } from 'vue-router'
import MySearch from '../views/MySearch.vue'
import Landing from '../views/Landing.vue'
import Feedback from '../views/Feedback.vue'
import Query from '../views/Query.vue'
import SearchResults from '../views/SearchResults.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/mysearch',
      name: 'Find My Search',
      component: MySearch
    },
    {
      path: '/', 
      name: 'Landing',
      component: Landing
    },
    {
      path: '/feedback', 
      name: 'Provide Feedback',
      component: Feedback 
    },
    {
      path: '/searchresults', 
      name: 'SearchResults',
      component: SearchResults 
    },
    {
      path: '/newsearch', 
      name: 'Query',
      component: Query 
    }
  ]
})

export default router
