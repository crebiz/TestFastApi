import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import DashboardPage from '../views/dashboard/DashboardPage.vue'
import ProfilePage from '../views/profile/ProfilePage.vue'
import FundPage from '../views/fund/FundPage.vue'
import CodePage from '../views/code/CodePage.vue'
import CardPage from '../views/card/CardPage.vue'
import FlowPage from '../views/flow/FlowPage.vue'
import BudgetPage from '../views/budget/BudgetPage.vue'

// 스토어 가져오기
import { useAuthStore } from '../stores/authStore'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: HomePage
  },
  {
    path: '/dashboard',
    component: DashboardLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'dashboard',
        component: DashboardPage
      },
      {
        path: 'budget',
        name: 'budget',
        component: BudgetPage
      },
      {
        path: 'profile',
        name: 'profile',
        component: ProfilePage
      },
      {
        path: 'fund',
        name: 'fund',
        component: FundPage
      },
      {
        path: 'card',
        name: 'card',
        component: CardPage
      },
      {
        path: 'code',
        name: 'code',
        component: CodePage
      },
      {
        path: 'flow',
        name: 'flow',
        component: FlowPage
      },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 네비게이션 가드 설정
router.beforeEach((to, from, next) => {
  // Pinia 스토어는 앱 인스턴스 외부에서 사용할 때 특별한 처리가 필요합니다
  const authStore = useAuthStore()
  
  // 인증이 필요한 페이지인지 확인
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  
  // 로그인 상태 확인
  const isAuthenticated = authStore.isAuthenticated
  
  if (requiresAuth && !isAuthenticated) {
    // 인증이 필요한데 로그인되지 않은 경우 홈페이지로 리디렉션
    next('/')
  } else {
    // 그 외의 경우 정상적으로 라우팅
    next()
  }
})

export default router
