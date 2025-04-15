import logging
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 로깅 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("hydrogen_controller.log", encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

router = APIRouter(
    prefix="/hydrogen-stations",
    tags=["hydrogen-stations"],
)

@router.get("/")
async def get_hydrogen_stations():
    """
    수소충전소 정보 목록을 반환합니다.
    
    Returns:
        JSONResponse: 수소충전소 정보 목록
    """
    # API에서 데이터를 가져옵니다
    data = await get_hydrogen_station_data()
    return data

@router.get("/data")
async def get_hydrogen_station_data():
    """
    수소충전소 정보 데이터를 가져옵니다.
    
    Returns:
        dict: 수소충전소 정보 데이터
    """
    try:
        logger.info("수소충전소 데이터 API 요청 시작")
        
        # .env 파일에서 API 정보 가져오기
        api_url = os.getenv("HYDROGEN_API_URL")
        api_key = os.getenv("HYDROGEN_API_KEY")
        
        if not api_url or not api_key:
            logger.error("API URL 또는 API 키가 설정되지 않았습니다.")
            raise HTTPException(status_code=500, detail="API 설정이 올바르지 않습니다.")
        
        # API 요청 헤더 설정
        headers = {
            'Authorization': api_key,
            'Content-Type': 'application/json'
        }
        
        # API 요청 보내기
        async with httpx.AsyncClient(timeout=30.0) as client:
            logger.info(f"API 요청: {api_url}")
            response = await client.get(api_url, headers=headers)
            
            # 응답 상태 확인
            if response.status_code != 200:
                logger.error(f"API 응답 오류: {response.status_code}, {response.text}")
                raise HTTPException(status_code=response.status_code, detail="수소충전소 API 요청 실패")
            
            # 응답 데이터 파싱
            data = response.json()
            logger.info("API 응답 데이터 수신 완료")
            
            # 응답 데이터 가공
            stations = []
            if 'data' in data and 'list' in data['data']:
                for station in data['data']['list']:
                    station_info = {
                        'name': station.get('statNm', '정보 없음'),
                        'address': station.get('addr', '정보 없음'),
                        'price': f"{station.get('price', '정보 없음')}원/kg",
                        'status': station.get('statStusCd', '정보 없음'),
                        'operation_time': station.get('operTime', '정보 없음'),
                        'phone': station.get('telNo', '정보 없음'),
                        'latitude': station.get('lat', ''),
                        'longitude': station.get('lng', ''),
                        'company': station.get('entrpsNm', '정보 없음'),
                        'capacity': station.get('cpcty', '정보 없음'),
                        'pressure': station.get('prsrVal', '정보 없음'),
                        'update_date': station.get('updtDt', '정보 없음')
                    }
                    stations.append(station_info)
            
            # 가격 차트 데이터 (예시 데이터, 실제 API에서 제공하는 경우 수정 필요)
            price_data = {
                'labels': ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
                'data': [8800, 8800, 8800, 8800, 8800, 8800, 8800, 8800, 8800, 8800, 8800, 8800]
            }
            
            # 전체 원본 데이터도 함께 반환
            return JSONResponse(
                content={
                    "stations": stations,
                    "price_data": price_data,
                    "raw_data": data  # 원본 API 응답 데이터 전체 포함
                },
                media_type="application/json; charset=utf-8"
            )
            
    except HTTPException as e:
        logger.error(f"HTTP 예외 발생: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"예외 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"수소충전소 데이터를 가져오는 중 오류가 발생했습니다: {str(e)}")
