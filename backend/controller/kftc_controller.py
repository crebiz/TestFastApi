from fastapi import APIRouter, Depends, HTTPException, Path
import logging
import os

from backend.service.kftc_service import kftc_service, KftcService

# --- 로깅 설정 시작 ---
# 로그 파일 경로 설정
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

router = APIRouter(
    prefix="/kftc",
    tags=["kftc"]
)

@router.get("/balance/{fintech_use_num}", summary="KFTC 계좌 잔액 조회")
async def get_kftc_balance(
    fintech_use_num: str = Path(..., title="핀테크 이용번호", description="조회할 계좌의 핀테크 이용번호"),
    service: KftcService = Depends(lambda: kftc_service) # 서비스 의존성 주입
):
    """
    제공된 핀테크 이용번호를 사용하여 KFTC 오픈뱅킹 API를 통해 계좌 잔액을 조회합니다.

    **주의:** 현재는 실제 KFTC API 대신 임시 데이터를 반환합니다.
    """
    try:
        logger.info(f"Received request to get balance for fintech_use_num: {fintech_use_num}")
        access_token = await service.get_auth_url()
        account_url = await service.get_account_url()
        # balance_info = await service.get_account_balance(fintech_use_num)
        return balance_info
    except HTTPException as e:
        # 서비스 레이어에서 발생한 HTTPException을 그대로 클라이언트에게 전달
        raise e
    except Exception as e:
        logger.exception(f"Unexpected error in get_kftc_balance endpoint: {e}")
        raise HTTPException(status_code=500, detail="잔액 조회 처리 중 오류 발생")
