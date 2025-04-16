import { defineStore } from 'pinia'
import axios from 'axios'

interface User {
  id: number
  username: string
  email: string
  imageUrl: string
}

interface LoginData {
  name: string
  email: string
  imageUrl: string
}

interface AuthState {
  user: User | null
  isAuthenticated: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    isAuthenticated: false
  }),
  
  actions: {
    async fetchGoogleClientId() {
      try {
        const response = await axios.get('http://localhost:8000/api/config')
        return response.data.GOOGLE_CLIENT_ID
      } catch (error) {
        console.error('Google Client ID 가져오기 실패:', error)
        throw error
      }
    },
    
    async googleLogin(userData: LoginData) {
      try {
        const response = await axios.post('http://localhost:8000/users/google-login', userData, {
          withCredentials: true
        })
        
        // 로그인 성공 처리
        localStorage.setItem('access_token', response.data.tokens.access_token)
        localStorage.setItem('refresh_token', response.data.tokens.refresh_token)
        
        // 사용자 정보 저장
        this.user = response.data.user
        this.isAuthenticated = true
        
        return response.data
      } catch (error) {
        console.error('Google 로그인 실패:', error)
        throw error
      }
    },
    
    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      this.user = null
      this.isAuthenticated = false
    }
  }
})
