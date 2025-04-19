import httpx
import os
from dotenv import load_dotenv
import logging
from fastapi import HTTPException, status

load_dotenv()

# --- 로깅 설정 시작 ---
# 로그 파일 경로 설정 (kftc_controller/service와 동일한 파일 사용)
LOG_DIR = os.path.join("backend", "logs")
LOG_FILE = os.path.join(LOG_DIR, "kftc.log")

# 로그 디렉토리 생성 (없는 경우)
os.makedirs(LOG_DIR, exist_ok=True)

# 로거 인스턴스 생성
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) # 로그 레벨 설정

# 기존 핸들러 제거 (중복 로깅 방지)
if logger.hasHandlers():
    logger.handlers.clear()

# 파일 핸들러 설정
file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
file_handler.setLevel(logging.INFO)

# 로그 포매터 설정
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 로거에 핸들러 추가
logger.addHandler(file_handler)

# 로그가 상위 로거로 전파되지 않도록 설정 (선택 사항)
logger.propagate = False
# --- 로깅 설정 끝 ---

class KftcApiClient:
    def __init__(self):
        self.client_id = os.getenv("KFTC_CLIENT_ID")
        self.client_secret = os.getenv("KFTC_CLIENT_SECRET")
        self.token_url = os.getenv("KFTC_TOKEN_URL")
        self.auth_url = os.getenv("KFTC_AUTH_URL")
        self.account_url = os.getenv("KFTC_ACCOUNT_URL")
        self.balance_api_url = os.getenv("KFTC_BALANCE_API_URL")

        if not all([self.client_id, self.client_secret, self.token_url, self.auth_url, self.account_url, self.balance_api_url]):
            logger.error("KFTC API credentials or URLs are missing in .env file")
            raise ValueError("KFTC API 설정값이 .env 파일에 누락되었습니다.")

        self._access_token = None

    async def get_auth_url(self) -> str:
        """OAuth 2.0 인증 URL을 생성합니다."""
        return f"{self.auth_url}?client_id={self.client_id}&redirect_uri={self.client_secret}&response_type=code"

    async def get_account_url(self) -> str:
        """OAuth 2.0 계좌 인증 URL을 생성합니다."""
        return f"{self.account_url}?client_id={self.client_id}&redirect_uri={self.client_secret}&response_type=code"

    async def _get_access_token(self) -> str:
        """OAuth 2.0 Client Credentials Grant를 사용하여 Access Token을 발급받습니다."""
        # TODO: 실제 토큰 발급 로직 구현 (토큰 만료 처리 포함)
        if self._access_token: # 간단한 캐싱 (실제로는 만료 시간 고려 필요)
            return self._access_token

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "oob" # scope는 KFTC에서 요구하는 값으로 변경 필요
        }

        async with httpx.AsyncClient() as client:
            try:
                logger.info(f"Requesting access token from {self.token_url}")
                logger.info(f"Requesting data {data}")
                response = await client.post(self.token_url, headers=headers, data=data)
                response.raise_for_status() # HTTP 오류 발생 시 예외 발생
                token_data = response.json()
                self._access_token = token_data.get("access_token")
                if not self._access_token:
                    logger.error(f"Failed to get access token: {token_data}")
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="KFTC 토큰 발급 실패")
                # TODO: 토큰 만료 시간(expires_in) 처리 로직 추가
                logger.info("Successfully obtained KFTC access token.")
                return self._access_token
            except httpx.RequestError as exc:
                logger.error(f"An error occurred while requesting KFTC token: {exc}")
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="KFTC 인증 서버 통신 오류")
            except httpx.HTTPStatusError as exc:
                logger.error(f"KFTC token request failed: {exc.response.status_code} - {exc.response.text}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="KFTC 토큰 발급 요청 실패")

    async def get_balance(self, fintech_use_num: str) -> dict:
        """핀테크 이용번호를 사용하여 계좌 잔액을 조회합니다."""
        access_token = await self._get_access_token()
        # TODO: 실제 잔액 조회 API 호출 로직 구현
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8"
        }
        # params 구성 (KFTC API 명세 확인 필요)
        params = {
            "bank_tran_id": "", # 은행거래고유번호 (자체 생성 규칙 필요)
            "tran_dtime": "",   # 요청일시 (YYYYMMDDHHMMSS)
            "fintech_use_num": fintech_use_num
        }

        logger.info(f"Requesting balance for fintech_use_num: {fintech_use_num}")
        # async with httpx.AsyncClient() as client:
        #     try:
        #         response = await client.get(self.balance_api_url, headers=headers, params=params)
        #         response.raise_for_status()
        #         balance_data = response.json()
        #         logger.info(f"Successfully retrieved balance for {fintech_use_num}")
        #         return balance_data
        #     except httpx.RequestError as exc:
        #         logger.error(f"An error occurred while requesting KFTC balance: {exc}")
        #         raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="KFTC 잔액 조회 통신 오류")
        #     except httpx.HTTPStatusError as exc:
        #         logger.error(f"KFTC balance request failed: {exc.response.status_code} - {exc.response.text}")
        #         # KFTC 오류 코드(rsp_code)에 따른 처리 필요
        #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="KFTC 잔액 조회 요청 실패")

        # 임시 응답
        return {"account_num": "123-456-789", "balance_amt": "10000"}

# KFTC API 클라이언트 인스턴스 생성 (싱글턴처럼 사용 가능)
kftc_client = KftcApiClient()
