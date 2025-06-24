import { defineStore } from 'pinia'
import { ref } from 'vue'

/**
 * 기본 정보 탭의 데이터 구조를 정의하는 인터페이스
 * 사용자의 개인 정보와 소개를 관리
 */
export interface BasicInfo {
  /** 사용자 이름 */
  name: string
  /** 이메일 주소 */
  email: string
  /** 전화번호 */
  phone: string
  /** 소속 부서 */
  department: string
  /** 자기소개 */
  introduction: string
}

/**
 * 상태 관리 탭의 데이터 구조를 정의하는 인터페이스
 * 프로젝트의 작업 상태를 카테고리별로 관리
 */
export interface StatusData {
  /** 완료된 작업 목록 */
  completedTasks: string[]
  /** 진행 중인 작업 목록 */
  inProgressTasks: string[]
  /** 대기 중인 작업 목록 */
  pendingTasks: string[]
}

/**
 * AI 설정 탭의 데이터 구조를 정의하는 인터페이스
 * AI 모델과 관련된 설정값들을 관리
 */
export interface AiSettings {
  /** 선택된 AI 모델명 */
  selectedModel: string
  /** AI 응답의 창의성을 조절하는 온도 값 (0.0 - 2.0) */
  temperature: number
  /** AI 응답의 최대 토큰 수 */
  maxTokens: number
}

/**
 * 전체 탭 데이터를 통합하는 최상위 인터페이스
 * 모든 탭의 데이터를 하나의 객체로 관리
 */
export interface TabData {
  /** 기본 정보 탭 데이터 */
  basicInfo: BasicInfo
  /** 상태 관리 탭 데이터 */
  status: StatusData
  /** AI 설정 탭 데이터 */
  aiSettings: AiSettings
}

/**
 * 탭 데이터 관리를 위한 Pinia 스토어
 * 임시저장, 데이터 조회, 초기화 등의 기능을 제공
 */
export const useTabDataStore = defineStore('tabData', () => {
  /**
   * 임시저장된 데이터를 보관하는 반응형 참조
   * 사용자가 '임시저장' 버튼을 클릭했을 때 모든 탭의 데이터가 여기에 저장됨
   * 초기값은 모든 필드가 빈 값으로 설정된 기본 구조
   */
  const tempData = ref<TabData>({
    basicInfo: {
      name: '',
      email: '',
      phone: '',
      department: '',
      introduction: ''
    },
    status: {
      completedTasks: [],
      inProgressTasks: [],
      pendingTasks: []
    },
    aiSettings: {
      selectedModel: '',
      temperature: 0,
      maxTokens: 0
    }
  })

  /**
   * 현재 모든 탭의 데이터를 임시저장하는 함수
   * 
   * TabPage 컴포넌트에서 '임시저장' 버튼 클릭 시 호출됨
   * 전달받은 데이터를 깊은 복사하여 tempData에 저장하고 콘솔에 로그 출력
   * 
   * @param {TabData} data - 저장할 탭 데이터 (basicInfo, status, aiSettings 포함)
   */
  const saveTempData = (data: TabData) => {
    tempData.value = { ...data }
    console.log('임시저장 완료:', tempData.value)
  }

  /**
   * 임시저장된 데이터를 조회하는 함수
   * 
   * TabPage 컴포넌트에서 '불러오기' 버튼 클릭 시 호출됨
   * 현재 tempData에 저장된 데이터를 반환하여 각 탭에 데이터를 복원
   * 
   * @returns {TabData} 현재 임시저장된 데이터
   */
  const getTempData = () => {
    return tempData.value
  }

  /**
   * 임시저장된 데이터를 모두 초기화하는 함수
   * 
   * TabPage 컴포넌트에서 '적용' 버튼 클릭 후 또는 명시적 초기화 시 호출됨
   * 모든 필드를 기본값(빈 문자열, 빈 배열, 0)으로 재설정
   * 임시저장 상태를 완전히 리셋하여 새로운 작업을 시작할 수 있게 함
   */
  const clearTempData = () => {
    tempData.value = {
      basicInfo: {
        name: '',
        email: '',
        phone: '',
        department: '',
        introduction: ''
      },
      status: {
        completedTasks: [],
        inProgressTasks: [],
        pendingTasks: []
      },
      aiSettings: {
        selectedModel: '',
        temperature: 0,
        maxTokens: 0
      }
    }
  }

  /**
   * 현재 임시저장된 데이터가 기본값과 다른지 확인하는 함수
   * 
   * 사용자가 탭을 변경하거나 페이지를 떠날 때 unsaved 데이터 경고를 표시할지 결정
   * 모든 필드가 기본값(빈 문자열, 빈 배열, 0)과 같으면 false, 하나라도 다르면 true 반환
   * 
   * @returns {boolean} 임시저장된 데이터가 있으면 true, 모두 기본값이면 false
   */
  const hasTempData = () => {
    const current = tempData.value
    const isEmpty = 
      current.basicInfo.name === '' &&
      current.basicInfo.email === '' &&
      current.basicInfo.phone === '' &&
      current.basicInfo.department === '' &&
      current.basicInfo.introduction === '' &&
      current.status.completedTasks.length === 0 &&
      current.status.inProgressTasks.length === 0 &&
      current.status.pendingTasks.length === 0 &&
      current.aiSettings.selectedModel === '' &&
      current.aiSettings.temperature === 0 &&
      current.aiSettings.maxTokens === 0
    
    return !isEmpty
  }

  /**
   * 스토어에서 외부로 노출할 상태와 메소드들을 반환
   * 
   * 다른 컴포넌트에서 이 스토어를 사용할 때 접근 가능한 API들
   * - tempData: 현재 임시저장된 데이터 (읽기 전용으로 사용 권장)
   * - saveTempData: 데이터 임시저장
   * - getTempData: 임시저장된 데이터 조회
   * - clearTempData: 임시저장 데이터 초기화
   * - hasTempData: 임시저장 데이터 존재 여부 확인
   */
  return {
    tempData,
    saveTempData,
    getTempData,
    clearTempData,
    hasTempData
  }
})
