import { makeAutoObservable, runInAction } from 'mobx';
import api from '../services/api';
import { Category } from '../types';

class CategoryStore {
  categories: Category[] = [];
  currentCategory: Category | null = null;
  loading = false;
  error: string | null = null;

  constructor() {
    makeAutoObservable(this);
  }

  fetchCategories = async () => {
    this.loading = true;
    this.error = null;
    try {
      const response = await api.get('/categories');
      runInAction(() => {
        this.categories = response.data;
        this.loading = false;
      });
    } catch (error) {
      runInAction(() => {
        this.error = '카테고리 목록을 불러오는데 실패했습니다.';
        this.loading = false;
      });
    }
  };

  fetchCategoryById = async (id: number) => {
    this.loading = true;
    this.error = null;
    try {
      const response = await api.get(`/categories/${id}`);
      runInAction(() => {
        this.currentCategory = response.data;
        this.loading = false;
      });
    } catch (error) {
      runInAction(() => {
        this.error = '카테고리 정보를 불러오는데 실패했습니다.';
        this.loading = false;
      });
    }
  };

  createCategory = async (categoryData: Partial<Category>) => {
    this.loading = true;
    this.error = null;
    try {
      const response = await api.post('/categories', categoryData);
      runInAction(() => {
        this.categories.push(response.data);
        this.loading = false;
      });
      return response.data;
    } catch (error) {
      runInAction(() => {
        this.error = '카테고리 생성에 실패했습니다.';
        this.loading = false;
      });
      return null;
    }
  };

  updateCategory = async (id: number, categoryData: Partial<Category>) => {
    this.loading = true;
    this.error = null;
    try {
      const response = await api.put(`/categories/${id}`, categoryData);
      runInAction(() => {
        const index = this.categories.findIndex(category => category.id === id);
        if (index !== -1) {
          this.categories[index] = response.data;
        }
        if (this.currentCategory?.id === id) {
          this.currentCategory = response.data;
        }
        this.loading = false;
      });
      return response.data;
    } catch (error) {
      runInAction(() => {
        this.error = '카테고리 정보 업데이트에 실패했습니다.';
        this.loading = false;
      });
      return null;
    }
  };

  deleteCategory = async (id: number) => {
    this.loading = true;
    this.error = null;
    try {
      await api.delete(`/categories/${id}`);
      runInAction(() => {
        this.categories = this.categories.filter(category => category.id !== id);
        if (this.currentCategory?.id === id) {
          this.currentCategory = null;
        }
        this.loading = false;
      });
      return true;
    } catch (error) {
      runInAction(() => {
        this.error = '카테고리 삭제에 실패했습니다.';
        this.loading = false;
      });
      return false;
    }
  };
}

// 인스턴스 생성 후 내보내기
const categoryStore = new CategoryStore();
export default categoryStore;
