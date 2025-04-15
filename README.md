# TestFastApi Backend Project

이 프로젝트는 FastAPI를 백엔드로 사용하여 PostgreSQL과 연동하여 테스트 하기 위해 생성한 프로젝트 입니다.
이 프로젝트는 Windsurf AI를 사용하여 생성되었습니다.
이 프로젝트는 Claude 3.5와 Claude 3.7를 사용하여 코딩하였습니다.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. .env 파일에 관한 내용입니다:
데이터베이스 접속 정보, JWT 설정 정보, Google OAuth 정보, 기타 사용중인 API 정보는 `.env` file에 작성합니다.
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

3. 데이터베이스 테이블 생성을 위해서는 `init_database.py`를 실행합니다.

4. server 실행하는 방법법:
```bash
uvicorn main:app --reload
```

5. API 문서를 확인하는 방법:
- http://localhost:8000/docs
- http://localhost:8000/redoc


## Project 구조

- `main.py`: FastAPI 애플리케이션의 진입점
- `database/`: 데이터베이스 설정 및 연결 관리
- `model/`: SQLAlchemy 모델
- `schemas/`: 요청/응답 검증을 위한 Pydantic 스키마
- `controller/`: API 라우트 핸들러
- `service/`: 비즈니스 로직
- `middleware/`: 사용자 정의 미들웨어
- `templates/`: Jinja2 템플릿
- `static/`: 정적 파일
