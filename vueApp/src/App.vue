<template>
  <router-view />
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@300;400;500;600;700&family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

:root {
  /* 폰트 변수 */
  --font-family-primary: 'IBM Plex Sans KR', sans-serif;
  --font-family-secondary: 'Noto Sans KR', sans-serif;
  
  /* 색상 팔레트 - 라이트 테마 */
  --color-primary: #205781;
  --color-secondary: #4F959D;
  --color-tertiary: #98D2C0;
  --color-background: #F6F8D5;
  --color-surface: #FFFFFF;
  
  /* RGB 색상 변수 (CSS 함수용) */
  --color-primary-rgb: 32, 87, 129;
  --color-secondary-rgb: 79, 149, 157;
  --color-tertiary-rgb: 152, 210, 192;
  --color-background-rgb: 246, 248, 213;
  
  /* 텍스트 색상 - 라이트 테마 */
  --text-dark: #1A2E3B;
  --text-medium: #4A5B67;
  --text-light: #7A8A96;
  --text-on-primary: #FFFFFF; /* 어두운 primary 배경에 밝은 텍스트 */
  --text-on-secondary: #FFFFFF; /* 어두운 secondary 배경에 밝은 텍스트 */
  --text-on-tertiary: #2A3F4D; /* 밝은 tertiary 배경에 어두운 텍스트 */
  --text-on-background: #2A3F4D; /* 밝은 background 배경에 어두운 텍스트 */
  
  /* 기능적 색상 */
  --color-success: #4CAF50;
  --color-warning: #FFC107;
  --color-error: #F44336;
  --color-info: #2196F3;
}

.theme--dark {
  /* 색상 팔레트 - 다크 테마 */
  --color-primary: #3A7CA5;
  --color-secondary: #6BABB2;
  --color-tertiary: #B0E0D0;
  --color-background: #1E2A32;
  --color-surface: #263238;
  
  /* RGB 색상 변수 (CSS 함수용) - 다크 테마 */
  --color-primary-rgb: 58, 124, 165;
  --color-secondary-rgb: 107, 171, 178;
  --color-tertiary-rgb: 176, 224, 208;
  --color-background-rgb: 30, 42, 50;
  
  /* 텍스트 색상 - 다크 테마 */
  --text-dark: #ECEFF1;
  --text-medium: #B0BEC5;
  --text-light: #78909C;
  --text-on-primary: #FFFFFF;
  --text-on-secondary: #FFFFFF;
  --text-on-tertiary: #263238;
  --text-on-background: #ECEFF1;
  
  /* 기능적 색상 - 다크 테마 */
  --color-success: #69F0AE;
  --color-warning: #FFD740;
  --color-error: #FF5252;
  --color-info: #40C4FF;
}

body {
  margin: 0;
  padding: 0;
  font-family: var(--font-family-primary);
  background-color: var(--color-background);
  color: var(--text-dark);
}

/* 기본 링크 스타일 */
a {
  color: var(--color-primary);
  text-decoration: none;
  transition: color 0.3s ease;
}

a:hover {
  color: var(--color-secondary);
}

/* 기본 버튼 스타일 */
button {
  background-color: var(--color-primary);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: var(--color-secondary);
}
</style>
