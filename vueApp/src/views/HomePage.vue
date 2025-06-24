<template>
  <div class="home-container">
    <div class="login-container">
      <h1>FastAPI Backend</h1>
      <p>Vue.js + TypeScript 프론트엔드와 FastAPI 백엔드로 구성된 애플리케이션입니다.</p>

      <div v-if="loading" class="loading">로딩 중...</div>
      <div v-else-if="error" class="error">오류: {{ error }}</div>
      <div v-else>
        <!-- 로그인되지 않은 상태 -->
        <div v-if="!authStore.isAuthenticated" class="login-button-container">
          <GoogleLogin v-if="googleClientId" :callback="handleGoogleLogin" :error-callback="handleGoogleError" prompt />
          <p class="login-description">Google 계정으로 로그인하세요</p>
        </div>

        <!-- 로그인된 상태 -->
        <div v-else class="user-info-container">
          <div class="user-info">
            <h3>환영합니다!</h3>
            <div v-if="authStore.user" class="user-details">
              <p><strong>이름:</strong> {{ authStore.user.username }}</p>
              <p><strong>이메일:</strong> {{ authStore.user.email }}</p>
              <div v-if="authStore.user.imageUrl" class="user-image">
                <img :src="authStore.user.imageUrl" alt="사용자 프로필" />
              </div>
            </div>
            <button @click="handleLogout" class="logout-button">로그아웃</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { decodeCredential } from 'vue3-google-login'
import { useRouter } from 'vue-router'

interface GoogleUserData {
  name?: string;
  email?: string;
  picture?: string;
  [key: string]: any;
}

export default defineComponent({
  name: 'HomePage',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    const googleClientId = ref<string | null>(null)
    const loading = ref(true)
    const error = ref<string | null>(null)

    // 초기화 및 로그인 상태 확인
    onMounted(async () => {
      // 1. 로컬 스토리지에서 토큰 확인
      const accessToken = localStorage.getItem('access_token')
      const refreshToken = localStorage.getItem('refresh_token')
      const userJson = localStorage.getItem('user')

      if (accessToken && refreshToken && userJson) {
        try {
          // 사용자 정보 불러오기
          const user = JSON.parse(userJson)
          authStore.user = user
          authStore.isAuthenticated = true
          
          // 이미 로그인된 상태라면 대시보드로 리디렉션
          router.push('/dashboard')
        } catch (err) {
          console.error('저장된 사용자 정보 불러오기 오류:', err)
          // 오류 발생 시 로컬 스토리지 정리
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          localStorage.removeItem('user')
        }
      }

      // 2. Google 클라이언트 ID 가져오기
      try {
        const clientId = await authStore.fetchGoogleClientId()
        googleClientId.value = clientId
        loading.value = false
      } catch (err) {
        error.value = 'Google 클라이언트 ID를 가져오는데 실패했습니다.'
        loading.value = false
      }
    })

    const handleGoogleLogin = async (response: any) => {
      try {
        // Google 응답에서 사용자 정보 추출
        const userData = decodeCredential(response.credential) as GoogleUserData

        // 백엔드에 로그인 요청
        const loginData = {
          name: userData.name || '',
          email: userData.email || '',
          imageUrl: userData.picture || ''
        }

        const result = await authStore.googleLogin(loginData)

        // 로컬 스토리지에 사용자 정보와 토큰 저장
        if (result && result.tokens) {
          localStorage.setItem('access_token', result.tokens.access_token)
          localStorage.setItem('refresh_token', result.tokens.refresh_token)
          localStorage.setItem('user', JSON.stringify(result.user))
          
          // 로그인 성공 후 대시보드로 리디렉션
          router.push('/dashboard')
        }

        // alert('로그인 성공!') // 대시보드로 이동하므로 알림은 제거
      } catch (err) {
        console.error('Google 로그인 오류:', err)
        error.value = 'Google 로그인에 실패했습니다.'
      }
    }

    const handleGoogleError = () => {
      error.value = 'Google 로그인에 실패했습니다.'
    }

    // 로그아웃 처리
    const handleLogout = () => {
      // 로컬 스토리지에서 데이터 제거
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')

      // 상태 초기화
      authStore.user = null
      authStore.isAuthenticated = false

      alert('로그아웃되었습니다.')
    }

    return {
      authStore,
      googleClientId,
      loading,
      error,
      handleGoogleLogin,
      handleGoogleError,
      handleLogout,
      router
    }
  }
})
</script>

<style scoped>
.home-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

.login-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 30px;
  width: 100%;
  max-width: 500px;
  text-align: center;
}

h1 {
  color: #333;
  margin-bottom: 10px;
}

p {
  color: #666;
  margin-bottom: 30px;
}

.login-button-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.user-info-container {
  margin-top: 20px;
}

.user-info {
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 20px;
  text-align: left;
}

.user-details {
  margin: 15px 0;
}

.user-image {
  margin-top: 15px;
  text-align: center;
}

.user-image img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logout-button {
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  font-size: 14px;
  cursor: pointer;
  margin-top: 15px;
  transition: background-color 0.3s;
}

.logout-button:hover {
  background-color: #d32f2f;
}

.login-description {
  margin-top: 15px;
  font-size: 14px;
  color: #666;
}

.loading,
.error {
  padding: 20px;
  border-radius: 4px;
  margin: 20px 0;
}

.loading {
  background-color: #e8f4fd;
  color: #0277bd;
}

.error {
  background-color: #ffebee;
  color: #c62828;
}
</style>
