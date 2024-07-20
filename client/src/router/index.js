import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'estimates',
      component: () => import('../views/EstimatesView.vue')
    },
    {
      path: '/filaments',
      name: 'filaments',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/FilamentsView.vue')
    },
    {
      path: '/customers',
      name: 'customers',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/CustomersView.vue')
    },
    {
      path: '/prints',
      name: 'prints',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/PrintsView.vue')
    },
    {
      path: '/filament/:id?',
      name: 'filament',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/FilamentView.vue'),
      props: route => {
        if (route.params.id)
          return { id: Number(route.params.id) }
        else
          return {};
      }
    },
    {
      path: '/customer/:id?',
      name: 'customer',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/CustomerView.vue'),
      props: route => {
        if (route.params.id)
          return { id: Number(route.params.id) }
        else
          return {};
      }
    },
    {
      path: '/print/:id?',
      name: 'print',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/PrintView.vue'),
      props: route => {
        if (route.params.id)
          return { id: Number(route.params.id) }
        else
          return {};
      }
    },
    {
      path: '/estimate/:id?',
      name: 'estimate',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/EstimateView.vue'),
      props: route => {
        if (route.params.id)
          return { id: Number(route.params.id) }
        else
          return {};
      }
    },
    {
      path: '/settings',
      name: 'settings',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/SettingsView.vue')
    }
  ]
})

export default router
