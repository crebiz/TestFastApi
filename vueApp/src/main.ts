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

// localStorage 안전하게 접근하기 위한 함수
function getStoredTheme(): string {
  try {
    if (typeof window !== 'undefined' && window.localStorage) {
      return localStorage.getItem('theme') || 'light'
    }
  } catch (e) {
    console.error('localStorage에 접근할 수 없습니다:', e)
  }
  return 'light'
}

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: getStoredTheme(),
    variations: {
      colors: ['primary', 'secondary'],
      lighten: 5,
      darken: 5,
    },
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#535C91',           // 포인트(블루그레이)
          secondary: '#9290C3',         // 서브 포인트(연보라)
          tertiary: '#1B1A55',          // 강조(딥 인디고)
          background: '#F5F6FA',        // 아주 연한 회색/화이트
          surface: '#FFFFFF',           // White surface
          error: '#F44336',             // 기본 Vuetify Error
          warning: '#FFC107',           // 기본 Vuetify Warning
          info: '#2196F3',              // 기본 Vuetify Info
          success: '#4CAF50',           // 기본 Vuetify Success
          'text-primary': '#070F2B',    // Primary 위 텍스트(딥 네이비)
          'text-secondary': '#9290C3',  // Secondary 위 텍스트
          'text-tertiary': '#F5F6FA',   // Tertiary 위 텍스트
          'text-background': '#1B1A55', // Background 위 텍스트
          'divider': '#9290C3'          // Divider
        }
      },
      dark: {
        dark: true,
        colors: {
          primary: '#535C91',           // 포인트(블루그레이)
          secondary: '#9290C3',         // 서브 포인트(연보라)
          tertiary: '#1B1A55',          // 보조 포인트(딥 인디고)
          background: '#070F2B',        // 딥 네이비/블랙(배경)
          surface: '#1B1A55',           // 더 어두운 서피스
          error: '#FF5252',             // 기본 Vuetify Error
          warning: '#FFD740',           // 기본 Vuetify Warning
          info: '#40C4FF',              // 기본 Vuetify Info
          success: '#69F0AE',           // 기본 Vuetify Success
          'text-primary': '#F5F6FA',    // Primary 위 텍스트
          'text-secondary': '#9290C3',  // Secondary 위 텍스트
          'text-tertiary': '#F5F6FA',   // Tertiary 위 텍스트
          'text-background': '#F5F6FA', // Background 위 텍스트
          'divider': '#535C91'          // Divider
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
