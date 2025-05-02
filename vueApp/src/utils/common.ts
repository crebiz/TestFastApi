/**
 * 공통 코드 관리 유틸리티
 * 그룹코드별 상세코드 값을 관리합니다.
 */

import axios from 'axios';
import { getApiUrl } from '@/config/api';

// 코드 타입 정의
export interface CodeDetail {
  id: string;        // 코드 값
  group_id: string;  // 그룹코드
  name: string;      // 코드명
  value?: string;    // 추가 값 (색상 코드 등)
  sort_order: number; // 정렬 순서
  use_yn: string;    // 사용 여부
  description: string | null; // 설명
  created_at?: string; // 생성일시
  updated_at?: string; // 수정일시
}

// 코드 캐시 (메모리에 코드 값 저장)
const codeCache: Record<string, CodeDetail[]> = {};

/**
 * 그룹코드에 해당하는 상세코드 목록을 조회합니다.
 * @param groupCode 그룹코드 (예: 'CARD_CODE')
 * @returns 상세코드 목록 Promise
 */
export const getCodeList = async (groupCode: string): Promise<CodeDetail[]> => {
  // 캐시에 있으면 캐시된 값 반환
  if (codeCache[groupCode]) {
    return codeCache[groupCode];
  }

  try {
    // API 호출하여 코드 목록 조회
    console.log(`코드 목록 조회 API 호출: ${getApiUrl('/api/codes/details')}?group_id=${encodeURIComponent(groupCode)}`);
    const response = await axios.get(`${getApiUrl('/api/codes/details')}?group_id=${encodeURIComponent(groupCode)}`);
    
    console.log(`API 응답 데이터:`, response.data);
    const codeList = response.data;
    
    // 응답 데이터 구조 확인
    console.log(`코드 목록 개수: ${codeList.length}`);
    if (codeList.length > 0) {
      console.log(`코드 목록 첫 번째 항목:`, codeList[0]);
      console.log(`코드 목록 키:`, Object.keys(codeList[0]));
    }
    
    // 캐시에 저장
    codeCache[groupCode] = codeList;
    
    return codeList;
  } catch (error) {
    console.error(`코드 목록 조회 오류 (${groupCode}):`, error);
    return [];
  }
};

/**
 * 코드값으로 코드명을 조회합니다.
 * @param groupCode 그룹코드 (예: 'CARD_CODE')
 * @param code 코드값 (예: 'SH')
 * @param defaultValue 기본값 (코드가 없을 경우 반환할 값)
 * @returns 코드명 또는 기본값
 */
export const getCodeName = async (
  groupCode: string, 
  code: string, 
  defaultValue: string = '기타'
): Promise<string> => {
  const codeList = await getCodeList(groupCode);
  const foundCode = codeList.find(item => item.id === code);
  return foundCode ? foundCode.name : defaultValue;
};

/**
 * 카드 코드로 카드명을 비동기로 조회합니다. (API 데이터 활용)
 * @param cardCode 카드 코드
 * @param defaultValue 기본값 (코드가 없을 경우 반환할 값)
 * @returns 카드명 Promise
 */
export const getCardName = async (cardCode: string, defaultValue: string = '기타 카드'): Promise<string> => {
  try {
    // CARD_CODE 그룹코드에서 카드명 조회
    return await getCodeName('CARD_CODE', cardCode, defaultValue);
  } catch (error) {
    console.error(`카드명 조회 오류 (${cardCode}):`, error);
    // 오류 발생 시 동기 방식으로 반환
    return getCardNameSync(cardCode, defaultValue);
  }
};

/**
 * 카드 코드로 카드명을 조회합니다. (동기 방식 - 비동기 함수 실패 시 백업용)
 * @param cardCode 카드 코드
 * @param defaultValue 기본값 (코드가 없을 경우 반환할 값)
 * @returns 카드명
 */
export const getCardNameSync = (cardCode: string, defaultValue: string = '기타 카드'): string => {
  switch (cardCode) {
    case 'SH': return '신한카드';
    case 'LT': return '롯데카드';
    case 'SS': return '삼성카드';
    case 'HD': return '현대카드';
    case 'HN': return '하나카드';
    case 'KB': return '국민카드';
    default: return defaultValue;
  }
};

/**
 * 카드사별 색상 코드를 반환합니다. (비동기 버전)
 * 코드 테이블의 value 값을 사용하여 색상을 결정합니다.
 * @param cardName 카드사 이름
 * @returns 색상 코드 Promise
 */
export const getCardColor = async (cardName: string): Promise<string> => {
  try {
    // 카드사 코드 목록 조회
    const cardCodes = await getCardCompanyCodes();
    
    // 카드사명으로 해당 카드사 코드 찾기
    const cardCode = cardCodes.find(code => code.name === cardName);
    
    // value 값이 있고 유효한 색상 코드인 경우 그 값 사용
    if (cardCode?.value && isValidColor(cardCode.value)) {
      return cardCode.value;
    }
    
    // 기본 색상 매핑 사용 (백업)
    return getCardColorSync(cardName);
  } catch (error) {
    console.error('카드사 색상 코드 조회 오류:', error);
    return getCardColorSync(cardName); // 오류 발생 시 동기 버전 사용
  }
};

/**
 * 카드사별 색상 코드를 반환합니다. (동기 버전)
 * 비동기 함수에서 오류 발생 시 백업으로 사용하거나, 동기적 처리가 필요한 경우 사용합니다.
 * @param cardName 카드사 이름
 * @returns 색상 코드
 */
export const getCardColorSync = (cardName: string): string => {
  switch (cardName) {
    case '신한카드': return 'blue-darken-1';
    case '롯데카드': return 'red-darken-1';
    case '삼성카드': return 'blue-darken-3';
    case '현대카드': return 'grey-darken-3';
    case '국민카드': return 'yellow-darken-3';
    case '하나카드': return 'green-darken-1';
    default: return 'primary';
  }
};

/**
 * 유효한 색상 코드인지 확인합니다.
 * @param color 확인할 색상 코드
 * @returns 유효성 여부
 */
const isValidColor = (color: string): boolean => {
  // Vuetify 색상 형식 검증 (예: 'blue-darken-1', 'red', 'green-lighten-2' 등)
  const colorPattern = /^[a-z]+(-(darken|lighten|accent)-[1-4])?$/;
  return colorPattern.test(color);
};

/**
 * 금액을 포맷팅합니다.
 * @param amount 금액
 * @returns 포맷팅된 금액 문자열
 */
export const formatAmount = (amount: number): string => {
  return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW' }).format(amount);
};

/**
 * 날짜를 포맷팅합니다.
 * @param dateString 날짜 문자열
 * @returns 포맷팅된 날짜 문자열
 */
export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'short'
  }).format(date);
};

/**
 * 카드사 코드 목록을 가져옵니다.
 * @returns 카드사 코드 목록 Promise (CodeDetail[] 형태)
 */
export const getCardCompanyCodes = async (): Promise<CodeDetail[]> => {
  try {
    console.log('카드사 코드 목록 조회 시작 (CARD_CODE)');
    
    // CARD_CODE 그룹코드에 해당하는 상세코드 목록 조회
    const codeList = await getCodeList('CARD_CODE');
    console.log('가져온 카드사 코드 목록:', codeList);
    
    // '전체' 옵션 추가
    const allOption: CodeDetail = {
      id: 'ALL',
      group_id: 'CARD_CODE',
      name: '전체',
      sort_order: 0,
      use_yn: 'Y',
      description: '전체 카드사',
      created_at: '',
      updated_at: ''
    };
    
    // '전체' 옵션을 추가한 새 배열 반환
    const result = [allOption, ...codeList];
    
    console.log('최종 카드사 코드 목록:', result);
    return result;
  } catch (error) {
    console.error('카드사 코드 목록 조회 오류:', error);
    
    // 오류 발생 시 기본 카드사 코드 반환 (배열 형태로)
    return [];
  }
};

/**
 * 코드 캐시를 초기화합니다.
 */
export const clearCodeCache = (): void => {
  Object.keys(codeCache).forEach(key => {
    delete codeCache[key];
  });
};
