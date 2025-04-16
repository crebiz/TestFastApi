import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import vue3GoogleLogin from 'vue3-google-login'

// 앱 생성
const app = createApp(App)

// Pinia 상태 관리 설정
const pinia = createPinia()
app.use(pinia)

// 라우터 설정
app.use(router)

// Google OAuth 설정
// 실제 클라이언트 ID는 백엔드에서 가져옵니다
app.use(vue3GoogleLogin, {
  clientId: 'placeholder-client-id'
})

// 앱 마운트
app.mount('#app')
