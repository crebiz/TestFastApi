/**
 * API 관련 환경 설정
 * 환경별(로컬, 개발, 운영)로 API 기본 URL을 설정합니다.
 */

// 현재 환경 (process.env.NODE_ENV는 Vue CLI에서 자동으로 설정됨)
// 'development', 'production', 'test' 중 하나의 값을 가짐
const env = process.env.NODE_ENV || 'development';

// 환경별 API 기본 URL 설정
const apiBaseUrls: { [key: string]: string } = {
  development: 'http://localhost:8000', // 로컬 개발 환경
  staging: 'https://api-dev.example.com', // 개발 서버 환경 (필요시 변경)
  production: 'https://api.example.com', // 운영 서버 환경 (필요시 변경)
};

// 현재 환경에 맞는 API 기본 URL 선택
export const API_BASE_URL = apiBaseUrls[env] || apiBaseUrls.development;

// API 경로 생성 함수
export const getApiUrl = (path: string): string => {
  // path가 이미 http:// 또는 https://로 시작하면 그대로 반환
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path;
  }
  
  // path가 /로 시작하지 않으면 /를 추가
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  
  // API 기본 URL과 경로 결합
  return `${API_BASE_URL}${normalizedPath}`;
};

export default {
  API_BASE_URL,
  getApiUrl,
};
