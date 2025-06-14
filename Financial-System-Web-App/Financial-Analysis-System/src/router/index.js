import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CreateQueryView from '../views/CreateQueryView.vue'
import QueryView from '../views/QueryView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/createQuery',
      name: 'createQuery',
      component: CreateQueryView
    },
    {
      path: '/query',
      name: 'query',
      // Passes props only in lower case - No camel case allowed
      props: route => ({ 
        query_id: Number(route.query.queryId), 
        query_name: route.query.queryName, 
        query_type: Number(route.query.queryType), 
        query_end_date: route.query.queryEndDate, 
        query_start_date: route.query.queryStartDate, 
        query_is_graph: Number(route.query.queryIsGraph)
      }),
      // Changing query by passing props instead of re-routing component means new component is created and new props are passed to the same one (saves on computation)
      component: QueryView
    },
  ]
})

export default router
