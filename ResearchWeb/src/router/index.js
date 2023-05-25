import { createRouter, createWebHistory } from 'vue-router'
import MySearch from '../views/MySearch.vue'
import Tutorial from '../views/Tutorial.vue'
import Feedback from '../views/Feedback.vue'
import Terms from '../views/Terms.vue'
import Privacy from '../views/Privacy.vue'  
import Query from '../views/Query.vue'
import Searching from '../views/Searching.vue'
import SearchPreference from '../views/SearchPreference.vue'
import Results from '../views/Results.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/preference',
      name: 'SearchPreference',
      component: SearchPreference,
      props: true
    },
    {
      path: '/mysearch',
      name: 'Find My Search',
      component: MySearch
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
    {
      path: '/results', 
      name: 'Results',
      component: Results 
    },
  ]
})

export default router
