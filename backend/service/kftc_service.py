import logging
from fastapi import HTTPException
import os

from backend.client.kftc_client import kftc_client

# --- 로깅 설정 시작 ---
# 로그 파일 경로 설정 (kftc_controller와 동일한 파일 사용)
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

class KftcService:

    async def get_account_balance(self, fintech_use_num: str) -> dict:
        """핀테크 이용번호를 사용하여 계좌 잔액 정보를 조회합니다."""
        try:
            logger.info(f"Attempting to get balance for fintech_use_num: {fintech_use_num}")
            # kftc_client.get_balance는 현재 임시 데이터를 반환합니다.
            # 실제 API 연동 후에는 여기서 반환되는 데이터를 가공하거나 그대로 전달할 수 있습니다.
            balance_data = await kftc_client.get_balance(fintech_use_num)
            logger.info(f"Successfully retrieved balance data (mock): {balance_data}")
            # TODO: 실제 API 응답 형식에 맞춰 필요한 데이터 추출 또는 가공
            return balance_data
        except HTTPException as e:
            # kftc_client에서 발생한 HTTPException을 그대로 전달
            logger.error(f"HTTPException occurred while getting balance: {e.detail}")
            raise e
        except Exception as e:
            logger.exception(f"An unexpected error occurred in get_account_balance: {e}")
            raise HTTPException(status_code=500, detail="잔액 조회 중 서버 오류가 발생했습니다.")

# 서비스 인스턴스 생성
kftc_service = KftcService()
