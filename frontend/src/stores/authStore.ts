import { makeAutoObservable, runInAction } from 'mobx';
import api from '../services/api';

interface User {
  id: number;
  email: string;
  username: string;
}

// 인증 관련 상태를 정의하는 인터페이스
// 이 인터페이스는 AuthStore 클래스의 속성들의 타입을 정의하는 데 사용됩니다.
class AuthStore {
  user: User | null = null;
  isAuthenticated: boolean = false;
  loading: boolean = false;
  error: string | null = null;
  googleClientId: string | null = null;

  constructor() {
    makeAutoObservable(this);
  }

  fetchGoogleClientId = async () => {
    this.loading = true;
    this.error = null;
    try {
      const response = await api.get('/api/config');
      runInAction(() => {
        this.googleClientId = response.data.GOOGLE_CLIENT_ID;
        this.loading = false;
      });
      return this.googleClientId;
    } catch (error) {
      runInAction(() => {
        this.error = 'Google 클라이언트 ID를 가져오는데 실패했습니다.';
        this.loading = false;
      });
      return null;
    }
  };

  googleLogin = async (googleResponse: any) => {
    this.loading = true;
    this.error = null;
    try {
      // 구글 로그인 응답에서 필요한 정보 추출
      const userData = {
        name: googleResponse.profileObj.name,
        email: googleResponse.profileObj.email,
        imageUrl: googleResponse.profileObj.imageUrl
      };

      // 백엔드 API 호출하여 로그인 처리
      const response = await api.post('/users/google-login', userData);
      
      runInAction(() => {
        this.user = response.data.user;
        this.isAuthenticated = true;
        
        // 토큰 저장
        localStorage.setItem('access_token', response.data.tokens.access_token);
        localStorage.setItem('refresh_token', response.data.tokens.refresh_token);
        
        // API 기본 헤더에 토큰 설정
        api.defaults.headers.common['Authorization'] = `Bearer ${response.data.tokens.access_token}`;
        
        this.loading = false;
      });
      
      return true;
    } catch (error) {
      runInAction(() => {
        this.error = '구글 로그인에 실패했습니다.';
        this.loading = false;
      });
      return false;
    }
  };

  logout = () => {
    // 로컬 스토리지에서 토큰 제거
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    
    // API 헤더에서 토큰 제거
    delete api.defaults.headers.common['Authorization'];
    
    // 상태 초기화
    this.user = null;
    this.isAuthenticated = false;
  };

  checkAuth = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      this.logout();
      return false;
    }

    try {
      // API 기본 헤더에 토큰 설정
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      
      // 사용자 정보 가져오기 (선택적)
      // const response = await api.get('/users/me');
      // this.user = response.data;
      this.isAuthenticated = true;
      return true;
    } catch (error) {
      this.logout();
      return false;
    }
  };
}

// 인스턴스 생성 후 내보내기
const authStore = new AuthStore();
export default authStore;
