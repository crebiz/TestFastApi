<template>
  <div class="home-container">
    <div class="login-container">
      <h1>FastAPI Backend</h1>
      <p>Vue.js + TypeScript 프론트엔드와 FastAPI 백엔드로 구성된 애플리케이션입니다.</p>
      
      <div v-if="loading" class="loading">로딩 중...</div>
      <div v-else-if="error" class="error">오류: {{ error }}</div>
      <div v-else class="login-button-container">
        <GoogleLogin
          v-if="googleClientId"
          :callback="handleGoogleLogin"
          :error-callback="handleGoogleError"
          prompt
        />
        <p class="login-description">Google 계정으로 로그인하세요</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { decodeCredential } from 'vue3-google-login'

export default defineComponent({
  name: 'HomePage',
  setup() {
    const authStore = useAuthStore()
    const googleClientId = ref<string | null>(null)
    const loading = ref(true)
    const error = ref<string | null>(null)

    onMounted(async () => {
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
        const userData = decodeCredential(response.credential)
        
        // 백엔드에 로그인 요청
        const loginData = {
          name: userData.name,
          email: userData.email,
          imageUrl: userData.picture
        }
        
        await authStore.googleLogin(loginData)
        alert('로그인 성공!')
      } catch (err) {
        console.error('Google 로그인 오류:', err)
        error.value = 'Google 로그인에 실패했습니다.'
      }
    }

    const handleGoogleError = () => {
      error.value = 'Google 로그인에 실패했습니다.'
    }

    return {
      googleClientId,
      loading,
      error,
      handleGoogleLogin,
      handleGoogleError
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

.login-description {
  margin-top: 15px;
  font-size: 14px;
  color: #666;
}

.loading, .error {
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
