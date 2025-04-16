import React, { useEffect, useState } from 'react';
import { observer } from 'mobx-react-lite';
import './HomePage.css';
import { GoogleLogin } from '@react-oauth/google';
import { GoogleOAuthProvider } from '@react-oauth/google';
import rootStore from '../../stores/rootStore';

const HomePage: React.FC = () => {
  const { authStore } = rootStore;
  const [googleClientId, setGoogleClientId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchGoogleClientId = async () => {
      try {
        const clientId = await authStore.fetchGoogleClientId();
        setGoogleClientId(clientId);
        setLoading(false);
      } catch (err) {
        setError('Google 클라이언트 ID를 가져오는데 실패했습니다.');
        setLoading(false);
      }
    };

    fetchGoogleClientId();
  }, [authStore]);

  const handleGoogleLogin = async (credentialResponse: any) => {
    try {
      // Google 응답에서 ID 토큰 추출
      const idToken = credentialResponse.credential;
      
      // ID 토큰을 디코딩하여 사용자 정보 추출
      const base64Url = idToken.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
      }).join(''));
      
      const { name, email, picture } = JSON.parse(jsonPayload);
      
      // 백엔드에 로그인 요청
      const userData = {
        name,
        email,
        imageUrl: picture
      };
      
      const response = await fetch('http://localhost:8000/users/google-login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
        credentials: 'include'
      });
      
      if (!response.ok) {
        throw new Error('로그인 처리 중 오류가 발생했습니다.');
      }
      
      const data = await response.json();
      
      // 로그인 성공 처리
      localStorage.setItem('access_token', data.tokens.access_token);
      localStorage.setItem('refresh_token', data.tokens.refresh_token);
      
      // 사용자 정보 저장
      authStore.user = data.user;
      authStore.isAuthenticated = true;
      
      alert('로그인 성공!');
      
    } catch (err) {
      console.error('Google 로그인 오류:', err);
      setError('Google 로그인에 실패했습니다.');
    }
  };

  if (loading) {
    return <div className="home-container"><div className="login-container">로딩 중...</div></div>;
  }

  if (error) {
    return <div className="home-container"><div className="login-container">오류: {error}</div></div>;
  }

  return (
    <div className="home-container">
      <div className="login-container">
        <h1>FastAPI Backend</h1>
        <p>React + TypeScript 프론트엔드와 FastAPI 백엔드로 구성된 애플리케이션입니다.</p>
        
        {googleClientId ? (
          <GoogleOAuthProvider clientId={googleClientId}>
            <div className="login-button-container">
              <GoogleLogin
                onSuccess={handleGoogleLogin}
                onError={() => setError('Google 로그인에 실패했습니다.')}
                useOneTap
              />
              <p className="login-description">Google 계정으로 로그인하세요</p>
            </div>
          </GoogleOAuthProvider>
        ) : (
          <div>Google 클라이언트 ID를 가져오는데 실패했습니다.</div>
        )}
      </div>
    </div>
  );
};

export default observer(HomePage);
