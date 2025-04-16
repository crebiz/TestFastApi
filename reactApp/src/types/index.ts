// 사용자 타입
export interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  created_at: string;
}

// 카테고리 타입
export interface Category {
  id: number;
  name: string;
  description: string;
}

// 수소 스테이션 타입
export interface HydrogenStation {
  id: number;
  name: string;
  address: string;
  latitude: number;
  longitude: number;
  category_id: number;
  category?: Category;
}
