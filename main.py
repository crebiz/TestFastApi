"""
TestFastApi 프로젝트 메인 실행 파일
백엔드 서버를 실행합니다.
"""

import uvicorn

if __name__ == "__main__":
    # 백엔드 서버 실행
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
