import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import vue3GoogleLogin from 'vue3-google-login'
import axios from 'axios'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#4CAF50',
          secondary: '#9C27B0',
          accent: '#9C27B0',
          error: '#F44336',
          warning: '#FF9800',
          info: '#00CAE3',
          success: '#4CAF50'
        }
      }
    }
  }
})

// 백엔드에서 Google 클라이언트 ID 가져오기
async function initApp() {
  try {
    // Google 클라이언트 ID 가져오기
    const response = await axios.get('http://localhost:8000/api/config')
    const googleClientId = response.data.GOOGLE_CLIENT_ID
    
    // 앱 생성
    const app = createApp(App)
    
    // Pinia 상태 관리 설정
    const pinia = createPinia()
    app.use(pinia)
    
    // Vuetify 설정
    app.use(vuetify)
    
    // 라우터 설정
    app.use(router)
    
    // Google OAuth 설정
    app.use(vue3GoogleLogin, {
      clientId: googleClientId
    })
    
    // 앱 마운트
    app.mount('#app')
    
    console.log('Vue 앱 초기화 완료: Google 클라이언트 ID 설정 완료')
  } catch (error) {
    console.error('Vue 앱 초기화 실패:', error)
    document.body.innerHTML = '<div style="padding: 20px; color: red;">Google 클라이언트 ID를 가져오는데 실패했습니다. 백엔드 서버가 실행 중인지 확인해주세요.</div>'
  }
}

// 앱 초기화 실행
initApp()
