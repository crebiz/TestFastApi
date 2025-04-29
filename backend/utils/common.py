from datetime import datetime, timezone

def get_current_time(as_string=False, format='%Y%m%d%H%M%S'):
    """
    현재 시간을 반환하는 공통 함수
    
    Args:
        as_string (bool): True인 경우 문자열 형식으로 반환, False인 경우 datetime 객체로 반환
        format (str): as_string이 True일 때 사용할 날짜 형식
    
    Returns:
        datetime 또는 str: 현재 시간 (as_string에 따라 타입이 결정됨)
    """
    now = datetime.now(timezone.utc)
    if as_string:
        return now.strftime(format)
    return now
