# TestFastApi 프로젝트

이 프로젝트는 FastAPI 백엔드와 세 가지 다른 프론트엔드 기술로 구성된 멀티 플랫폼 애플리케이션입니다.

## 프로젝트 구조

- `backend/`: FastAPI 백엔드 코드
  - `controller/`: API 라우트 핸들러
  - `database/`: 데이터베이스 설정 및 연결 관리
  - `model/`: SQLAlchemy 모델
  - `schemas/`: 요청/응답 검증을 위한 Pydantic 스키마
  - `service/`: 비즈니스 로직
  - `middleware/`: 사용자 정의 미들웨어
  - `main.py`: FastAPI 애플리케이션의 진입점

- `reactApp/`: React + TypeScript 웹 프론트엔드
  - `src/`: 소스 코드
    - `components/`: React 컴포넌트
    - `stores/`: MobX 상태 관리 스토어
    - `services/`: API 통신 서비스
    - `types/`: TypeScript 타입 정의

- `vueApp/`: Vue.js + TypeScript 웹 프론트엔드
  - `src/`: 소스 코드
    - `views/`: Vue 컴포넌트 뷰
    - `stores/`: Pinia 상태 관리 스토어
    - `router/`: Vue Router 설정

- `flutterApp/`: Flutter 모바일 앱
  - `lib/`: 소스 코드
    - `screens/`: 앱 화면 위젯
    - `services/`: API 통신 서비스
    - `models/`: 데이터 모델
    - `providers/`: Riverpod 상태 관리

## 백엔드 설정

1. 의존성 설치:
```bash
cd backend
pip install -r requirements.txt
```

2. .env 파일 설정:
- 데이터베이스 접속 정보, JWT 설정 정보, Google OAuth 정보, 기타 사용중인 API 정보는 `backend/.env` 파일에 작성합니다.
```
DB_HOST=localhost
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432

# JWT Settings
SECRET_KEY="your_secret_key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Google OAuth Settings
GOOGLE_CLIENT_SECRET="your_client_secret"

# Add any other required environment variables
```

3. 데이터베이스 테이블 생성:
```bash
cd backend
python init_database.py
```

4. 백엔드 서버 실행:
```bash
python main.py
```

5. API 문서 확인:
- http://localhost:8000/docs
- http://localhost:8000/redoc

## 프론트엔드 설정

### React 프론트엔드

1. 의존성 설치:
```bash
cd reactApp
npm install
```

2. 개발 서버 실행:
```bash
cd reactApp
npm start
```

3. 프론트엔드 빌드:
```bash
cd reactApp
npm run build
```

### Vue.js 프론트엔드

1. 의존성 설치:
```bash
cd vueApp
npm install
```

2. 개발 서버 실행:
```bash
cd vueApp
npm run serve
```

3. 프론트엔드 빌드:
```bash
cd vueApp
npm run build
```

### Flutter 모바일 앱

1. 의존성 설치:
```bash
cd flutterApp
flutter pub get
```

2. 앱 실행:
```bash
cd flutterApp
flutter run
```

3. 앱 빌드:
```bash
cd flutterApp
flutter build apk  # Android 앱 빌드
flutter build ios  # iOS 앱 빌드 (macOS 필요)
```

## 기술 스택

- 백엔드: FastAPI, SQLAlchemy, PostgreSQL
- 웹 프론트엔드: 
  - React, TypeScript, MobX
  - Vue.js, TypeScript, Pinia
- 모바일 앱: Flutter, Dart, Riverpod
- 인증: JWT, Google OAuth
- 공통 기능: 구글 로그인

## Windsurf AI
- 이 프로젝트는 Windsurf AI 툴을 사용하여 생성하였습니다.
- 이 프로젝트는 Claude 3.5와 Claude 3.7를 사용하여 코딩하였습니다.
- 생성된 코드에서 수정이 필요한 부분에 직접 코딩하였습니다.

## License
