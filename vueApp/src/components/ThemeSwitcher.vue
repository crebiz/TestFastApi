<template>
  <v-btn icon @click="toggleTheme">
    <v-icon>{{ isDarkTheme ? 'mdi-weather-sunny' : 'mdi-weather-night' }}</v-icon>
  </v-btn>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useTheme } from 'vuetify'

// Vuetify 테마 가져오기
const theme = useTheme()

// 현재 테마 상태 추적
const isDarkTheme = computed(() => theme.global.name.value === 'dark')

// 테마 전환 함수
function toggleTheme() {
  // 테마 전환
  const newTheme = isDarkTheme.value ? 'light' : 'dark'
  theme.global.name.value = newTheme
  
  // 로컬 스토리지에 테마 저장 (안전하게)
  try {
    if (typeof window !== 'undefined' && window.localStorage) {
      localStorage.setItem('theme', newTheme)
    }
  } catch (e) {
    console.error('localStorage에 접근할 수 없습니다:', e)
  }
  
  // 테마 클래스 적용
  if (typeof document !== 'undefined' && document.documentElement) {
    document.documentElement.classList.toggle('theme--dark', newTheme === 'dark')
  }
}

// 초기화 시 테마 클래스 적용
onMounted(() => {
  if (typeof document !== 'undefined' && document.documentElement) {
    document.documentElement.classList.toggle('theme--dark', theme.global.name.value === 'dark')
  }
})
</script>
